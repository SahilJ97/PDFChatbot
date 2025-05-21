from dataclasses import dataclass
from openai import OpenAI
from pypdf import PdfReader
from typing import Iterator
import numpy as np
from utils import silence_c_stderr

@dataclass
class PDFSection:
    page_numbers: list[int]
    text: str

class IndexedPDF:
    _pdf_sections: list[PDFSection] = []
    _embedding_matrix: np.array = []  # matrix of shape (number_of_sections, embedding_size)

    def __init__(
            self,
            pdf_path: str,
            open_ai_client: OpenAI,
            open_ai_embedding_model: str = "text-embedding-3-small",
            window_size: int = 2,
            window_overlap: int = 1,
    ):
        self.pdf_path = pdf_path
        self._open_ai_client = open_ai_client
        self.embedding_model = open_ai_embedding_model

        embeddings = []
        for section in self._extract_pdf_sections(window_size, window_overlap):
            embedding_response = self._open_ai_client.embeddings.create(
                input=section.text,
                model=self.embedding_model
            )
            section_embedding = np.array(embedding_response.data[0].embedding)
            section_embedding = section_embedding / np.linalg.norm(section_embedding)  # Normalize
            embeddings.append(section_embedding)
            self._pdf_sections.append(section)

        self._embedding_matrix = np.array(embeddings)

    def _extract_pdf_sections(
        self,
        window_size: int,
        window_overlap: int
    ) -> Iterator[PDFSection]:
        if window_overlap >= window_size:
            raise ValueError("window_overlap must be less than window_size")

        # Suppress pypdf's stderr output, as it tends to be a bit noisy
        with silence_c_stderr():
            reader = PdfReader(self.pdf_path)

        number_of_pages = len(reader.pages)
        offset = 0

        while offset < number_of_pages:
            section_content = []
            for i in range(window_size):
                if i + offset >= number_of_pages:
                    break
                page = reader.pages[offset + i]
                section_content.append(page.extract_text())

            yield PDFSection(
                page_numbers=[offset + i for i in range(window_size)],
                text=" ".join(section_content)
            )

            offset += window_size - window_overlap

    def most_relevant_text(self, query: str, k: int = 5) -> list[PDFSection]:
        query_embedding_result = self._open_ai_client.embeddings.create(
            input=query,  # To keep things simple, we embed the query as-is (no context)
            model=self.embedding_model
        )
        query_embedding = query_embedding_result.data[0].embedding
        similarity_scores = np.dot(self._embedding_matrix, query_embedding)
        top_k_indices = np.argsort(similarity_scores)[-k:][::-1]
        return [self._pdf_sections[idx] for idx in top_k_indices]
