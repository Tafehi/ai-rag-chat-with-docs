import os
from dotenv import load_dotenv
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.Populate import OpensearchManager
from langchain_ollama import OllamaEmbeddings


class TextEmbedding:
    def __init__(self):
        load_dotenv()
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._embedding_model = OllamaEmbeddings(model=os.getenv("OLLAMA_LLM_MODEL"))
        self._documents_folder = os.getenv("documents_folder")

    def ingest_docs(self):
        loader = ReadTheDocsLoader(self._documents_folder)
        raw_documents = loader.load()
        print(f"Loaded {len(raw_documents)} documents from {self._documents_folder}")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        documents = text_splitter.split_documents(raw_documents)
        print(f"Embedding model: {os.getenv('OLLAMA_LLM_MODEL')}")

        for doc in documents:
            new_url = doc.metadata["source"].replace("documents/latest/", "https:/")
            doc.metadata.update({"source": new_url})

        print(f"The loaded docs are split into {len(documents)} chunks for OpenSearch.")

        # Determine embedding dimension dynamically
        embedding_dim = len(self._embedding_model.embed_query("test"))
        print(f"Embedding dimension: {embedding_dim}")

        # Initialize OpenSearch manager with correct dimension
        manager = OpensearchManager(embedding_dim)
        print(f"Creating index '{self._index_name}' if it does not exist...")
        manager.create_index_if_not_exists(self._index_name)

        # Index documents
        manager.index_documents_from_folder(documents, self._embedding_model)
        print(f"Documents indexed in OpenSearch under index '{self._index_name}'.")
