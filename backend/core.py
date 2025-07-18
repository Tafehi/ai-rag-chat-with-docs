import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from model.Bedrock import BedrockLLM
from utils.Opensearch import OpensearchClient
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import OpenSearchVectorSearch


class Chatbot:
    def __init__(self):
        load_dotenv()
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._embedding_model = OllamaEmbeddings(model=os.getenv("OLLAMA_LLM_MODEL"))
        self._opensearch_client = OpensearchClient().client
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._opensearch_host = os.getenv("OPENSEARCH-HOST")
        self._opensearch_username = os.getenv("OPENSEARCH-USERNAME")
        self._opensearch_password = os.getenv("OPENSEARCH-PASSWORD")

    def index_exists(self) -> bool:
        """Check if the OpenSearch index exists."""
        return self._opensearch_client.indices.exists(index=self._index_name)

    def get_chatbot(self, query: str) -> dict:
        """Initialize and return the chatbot response."""
        chat = BedrockLLM().get_llm()
        if not chat or not self._embedding_model:
            raise RuntimeError(
                "Failed to initialize LLM due to missing chat model or embedding index."
            )

        try:
            # Check if index exists
            if not self.index_exists():
                raise RuntimeError(
                    f"Index '{self._index_name}' does not exist. Please ingest documents first."
                )

            # Set up vectorstore and retriever

            vectorstore = OpenSearchVectorSearch(
                opensearch_url=f"https://{self._opensearch_username}:{self._opensearch_password}@{self._opensearch_host}",
                index_name=self._index_name,
                embedding_function=self._embedding_model,
                vector_field="embedding",
                field_map={"vector": "embedding"},
            )

            doc_search = vectorstore.as_retriever()

            # Load prompt and build chain
            retrival_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            stuff_docs_chain = create_stuff_documents_chain(
                chat, retrival_qa_chat_prompt
            )
            qa = create_retrieval_chain(
                retriever=doc_search, combine_docs_chain=stuff_docs_chain
            )

            # Run query
            result = qa.invoke({"input": query})
            full_results = {
                "query": result["input"],
                "result": result["answer"],
                "source_documents": result["context"],
            }
            return full_results

        except Exception as e:
            raise RuntimeError(f"Failed to initialize chatbot: {e}")
