import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from 

load_dotenv()

retrieval_chain = create_retrieval_chain(
    api_key=os.getenv("API_KEY"),
    api_url=os.getenv("API_URL"),
)
