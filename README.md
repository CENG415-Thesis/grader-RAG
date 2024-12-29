# grader-RAG

This repository is about optimizing the RAG data pipeline for telecom to allow and process multiple queries.

RAG Pipeline takes multiple queries from `question_set.json` itself and directs the query one by one to the **Ollama-> llama3** model.

The output of the query is returned to the same model to be evaluated according to the following metrics:
- Groundedness
- Answer Relevance
- Context Relevance
- 
Then you can see all the results in different tables on a streamlit page.

## How can I run it?

First, the database is set up with the `python populate_database.py --reset` command.
This command clears the existing database and creates a new one.

Then, `process_and_grade.ipynb`  is run in order and the questions in the `question_set.json`  file are asked one by one and saved to 👉🏻 `processed_questions`.

Finally, the streamlit page can be run with the `streamlit run streamlit_app.py` command.
