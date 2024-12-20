from dataclasses import dataclass
from langchain_core.documents.base import Document
from langchain_core.messages import BaseMessage
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_aws import ChatBedrock

from src.utils import get_bedrowck_emb_fun
import src.config as cf

''' 
This script will run a RAG query: given an input user query, it will find
several most similar embeddings in the database, retrieve the text chunks 
corresponding to those embeddings, and create the enhanced query using
the `TEMPLATE_PROMPT` specified in `src.config.config.py`
'''

@dataclass
class QueryResponse:
    query_msg: str 
    response_msg: str 
    sources: list[(str, float)]


def get_query_matches(query_text: str) -> list[tuple[Document, float]]:
    db = Chroma(persist_directory=cf.CHROMA_PATH, embedding_function=get_bedrowck_emb_fun())
    rag_results = db.similarity_search_with_score(query_text, k=5)
    return rag_results 


def prepare_rag_prompt(query_text:str , rag_results: list[tuple[Document, float]]) -> str:
    context_text = '\n\n---\n\n'.join([doc.page_content for doc, _score in rag_results])
    prompt_template = ChatPromptTemplate.from_template(cf.PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    return prompt

def query_from_rag_prompt(prompt: str) -> BaseMessage:
    model = ChatBedrock(model_id=cf.BEDROCK_MODEL_ID)
    response = model.invoke(prompt)
    return response


def run_query(query_text: 
              str="How does the AI act define Artificial Intelligence") -> QueryResponse:
    rag_results = get_query_matches(query_text)
    prompt = prepare_rag_prompt(query_text, rag_results)
    response = query_from_rag_prompt(prompt)
    return QueryResponse(query_msg=query_text, response_msg=response.content,
                         sources=[(d.metadata.get('id', None), score) for d, score in rag_results])

if __name__ == "__main__":
    result = run_query("What does the the EU AI regulation say about AI systems for biometric identification")