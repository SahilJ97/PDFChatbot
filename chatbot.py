from sys import argv
from openai import OpenAI
from indexed_pdf import IndexedPDF, PDFSection
from dotenv import load_dotenv
import os
import traceback

pdf_path = argv[1]
load_dotenv()

# Initialize OpenAI client
OPEN_AI_ORG = os.environ.get("OPEN_AI_ORG")
OPEN_AI_KEY = os.environ.get("OPEN_AI_KEY")
open_ai_client = OpenAI(
    organization=OPEN_AI_ORG,
    api_key=OPEN_AI_KEY
)

PROMPT_TEMPLATE = """{question}
Answer the above question as truthfully as possible using the context provided below.
Include nothing but the answer in your response.
If the context is not helpful, respond with \"N/A\" (verbatim) and nothing else. Do not infer the answer if it isn't present in the context.

Context:
{context}"""

def answer_question_with_retrieved_sections(
    question: str,
    retrieved_sections: list[PDFSection],
    open_ai_model: str = "gpt-4.1-mini",
) -> str:
    for retrieved_section in retrieved_sections:
        prompt = PROMPT_TEMPLATE.format(question=question, context=retrieved_section.text)
        response_text = open_ai_client.responses.create(
            input=prompt,
            model=open_ai_model
        ).output_text

        if response_text != "N/A":
            page_str = str(retrieved_section.page_numbers[-1] + 1)
            if len(retrieved_section.page_numbers) > 1:
                page_str = ', '.join(str(num + 1) for num in retrieved_section.page_numbers[:-1]) + ' and/or ' + page_str
            return response_text.strip() + f"\nI found this answer somewhere on page {page_str}."

    return "I can't find the answer to your question. Sorry!"

# Load and index PDF
try:
    indexed_pdf = IndexedPDF(pdf_path, open_ai_client)
except Exception as e:
    print("An error occurred while loading or indexing the PDF!")
    exit(1)

print(f"Ingested {pdf_path}. Please ask your questions.")

# Chatbot loop
while True:
    query = input(">>> ")

    if query.strip() == "exit":
        exit(0)

    try:
        most_relevant_sections = indexed_pdf.most_relevant_text(query, 5)
    except Exception as e:
        print("An error occurred while searching the PDF!")
        exit(1)

    try:
        print(answer_question_with_retrieved_sections(query, most_relevant_sections))
    except Exception as e:
        print("An error occurred after retrieving the most relevant sections of the PDF!")
        exit(1)