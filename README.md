This simple solution uses OpenAI's API for both embedding and generation.
We use a windowing approach (1-page non-overlapping chunks) to maintain a relatively low number of requests to the embeddings endpoint.
We also experimented with overlapping chunks of 2-3 pages to accommodate cases in which a relevant passage is split across two 
consecutive pages, but found that larger windows resulted in retrieval being much less effective.
Due to the scale and nature of 
the assignment (no more than 1000 documents per session, no need for persistence), we forgo the use of sophisticated vector 
databases & NNS implementations in favor of an in-memory embedding matrix & complete similarity search. A similar system
with greater performance requirements should probably use an optimized vector database with smaller, sensible chunks (perhaps with overlap) for 
fast and precise lookup. Such a system should also implement guardrails to reduce hallucination and adversarial 
attacks.

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
Slavery in Africa was generally not permanent or inherited, with children of those enslaved usually being free and often intermarrying with their captors. In contrast, slavery in the Americas became permanent, with enslaved status inherited by the children of enslaved people, and was identified with race, creating a distinct, race-based slavery system.
I found this answer somewhere on page 20.
>>> What was the religious significance of gold in the Incan Empire?
The Inca worshipped the sun god Inti and called gold the “sweat” of the sun.
I found this answer somewhere on page 8.
>>> Why do extreme trans-Neptunian objects have elongated orbits?
I can't find the answer to your question. Sorry!
>>> exit

```

### Misc.

PDF courtesy of [OpenStax](https://openstax.org/subjects/humanities#U.S.%20History)