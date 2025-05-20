This simple solution uses OpenAI's API for both embedding and generation.
I use a windowing approach (2-page chunks with 1-page overlap) to maintain a relatively low number of requests to the embeddings 
endpoint while accommodating cases in which a relevant passage is split across two 
consecutive pages.
Due to the scale and nature of the assignment (no more than 1000 documents per session, no need for persistence), 
I forgo the use of sophisticated vector databases & NNS implementations in favor of an in-memory embedding matrix & 
complete similarity search. A similar system with greater performance requirements should probably use an optimized 
vector database with smaller, sensible chunks (perhaps with overlap) for fast and precise lookup. Such a system should 
also implement guardrails to reduce hallucination and adversarial attacks.

### Environment
This project has only been tested with Python 3.9. To set up your environment (e.g., conda, venv), run:
```
pip install -r requirements.txt
```
Note that if this project were to grow any larger and more complex, I would probably migrate it to [uv](https://docs.astral.sh/uv/).

### Example Usage
```
$ python chatbot.py USHistory-WEB-chapter1.pdf
Ingested USHistory-WEB-chapter1.pdf. Please ask your questions.
>>> How did slavery in Africa differ from slavery in the Americas?
Slavery in Africa was generally not permanent or inherited; children of enslaved people were usually free and could intermarry with their captors. In contrast, slavery in the Americas became permanent and race-based, with enslaved people identified by their skin color, and the children born to enslaved people automatically becoming enslaved. This change was driven by the demand for a permanent, plentiful labor supply for labor-intensive crops and shaped the unique character of slavery in the New World.
I found this answer somewhere on page 20 and/or 21.
>>> What was the religious significance of gold in the Incan Empire?
The Inca worshipped the sun god Inti and called gold the “sweat” of the sun.
I found this answer somewhere on page 7 and/or 8.
>>> Why do extreme trans-Neptunian objects have elongated orbits?
I can't find the answer to your question. Sorry!
>>> exit

```

### Misc.

PDF courtesy of [OpenStax](https://openstax.org/subjects/humanities#U.S.%20History)