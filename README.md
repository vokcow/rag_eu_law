# EU AI Law Chatbot 🇪🇺🤖🧑‍⚖️
## Intro
This repo implements a RAG pipeline using AWS bedrock llm models, gradio for the frontend, and AWS lambda for serveless hosting. The vector database indexes the recently approved EU AI law in the English and Spanish version using the `Titan Text Embeddings V2` model, whereas the chat model is `Antrophic's Claude 3 Haiku`. 

## Start Locally
* To run it locally, create a virtual environment, activate and, navigate to `rag_app` to run `pip install -e .`.
* Create the following directories `rag_app/data/input_data` and `rag_app/data/vector_db`.
* Put the PDFs in `rag_app/data/input_data` and then run `python rag_app/populate_database.py` which will put the vector embeddings in `rag_app/data/vector_db`.
* To create the docker image, from `rag_app` run `docker build -t rag_exp:latest . `, then `docker build -t rag_exp:latest .` to test it.

## Deploy to AWS Lambda
WIP