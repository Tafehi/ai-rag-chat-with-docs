import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from ollama import chat
from model.Bedrock import BedrockLLM
from utils.Opensearch import OpensearchClient
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch



class Chatbot:
    def __init__(self):
        load_dotenv()
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._embedding_model = OllamaEmbeddings(model=os.getenv("OLLAMA_LLM_MODEL"))

        
    def get_chatbot(self, query: str) -> str:
        """Initialize and return the chatbot."""
        # create a chat obj
        chat = BedrockLLM().get_llm()
        if not chat or not self._embedding_model:
            raise RuntimeError("Failed to initialize LLM due to missing chat model or embedding index.")
        try:
            # Initialize OpenSearch client
            opensearch_client = OpensearchClient().client
            # retriever docs from OpenSearch index
            vectorstore = OpenSearchVectorSearch(
                opensearch_url=os.getenv("OPENSEARCH-HOST"),
                index_name=self._index_name,
                embedding_function=self._embedding_model  # ✅ pass the whole object
            )


            doc_search = vectorstore.as_retriever()


            retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            
            stuff_docs_chain = create_stuff_documents_chain(chat, retrival_qa_chat_prompt)
            qa = create_retrieval_chain(
                retriever=doc_search, combine_docs_chain=stuff_docs_chain
            )
            result = qa.invoke({"input": query})

            return result.get("result", "No answer found.")

        except Exception as e:
            raise RuntimeError(f"Failed to initialize chatbot: {e}")


