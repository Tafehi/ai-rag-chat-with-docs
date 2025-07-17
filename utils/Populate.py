import os
import uuid
from dotenv import load_dotenv
from utils.Opensearch import OpensearchClient
from langchain.text_splitter import RecursiveCharacterTextSplitter


class OpensearchManager:
    """
    A class to manage the OpenSearch client connection and vector operations.
    """
    def __init__(self, embedding_dim=768):
        load_dotenv()
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._embedding_dimension = embedding_dim
        self._client = OpensearchClient().client

    def create_index_if_not_exists(self, index_name):
        if not self._client.indices.exists(index=index_name):
            index_body = {
                "settings": {
                    "index": {
                        "knn": True
                    }
                },
                "mappings": {
                    "properties": {
                        "text": {"type": "text"},
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": self._embedding_dimension,
                        }
                    }
                }
            }
            self._client.indices.create(index=index_name, body=index_body)
            print(f"Index '{index_name}' created with dimension {self._embedding_dimension}.")
        else:
            print(f"Index '{index_name}' already exists.")

    def index_documents_from_folder(self, documents, embedding_model):
        for doc in documents:
            try:
                if not doc.page_content.strip():
                    print(f"[SKIP] Empty content in document: {doc.metadata.get('source')}")
                    continue

                embedding_vector = embedding_model.embed_query(doc.page_content)

                if embedding_vector is None:
                    print(f"[SKIP] Embedding returned None for document: {doc.metadata.get('source')}")
                    continue

                if not isinstance(embedding_vector, list) or not all(isinstance(x, (float, int)) for x in embedding_vector):
                    print(f"[SKIP] Invalid embedding format for document: {doc.metadata.get('source')}")
                    continue

                if len(embedding_vector) != self._embedding_dimension:
                    print(f"[SKIP] Embedding dimension mismatch ({len(embedding_vector)}) for document: {doc.metadata.get('source')}")
                    continue

                doc_id = str(uuid.uuid4())
                doc_body = {
                    "text": doc.page_content,
                    "embedding": embedding_vector
                }
                self._client.index(index=self._index_name, id=doc_id, body=doc_body)
                print(f"[OK] Indexed document: {doc.metadata.get('source')} with ID: {doc_id}")

            except Exception as e:
                print(f"[ERROR] Failed to embed or index document: {e}")
