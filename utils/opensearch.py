import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch, RequestsHttpConnection


class OpensearchClient:
    """
    A class to manage the OpenSearch client connection and vector operations.
    """

    def __init__(self):
        load_dotenv()
        self._index_name = os.getenv("OPENSEARCH-INDEX-NAME")
        self._opensearch_host = os.getenv("OPENSEARCH-HOST")
        self._opensearch_username = os.getenv("OPENSEARCH-USERNAME")
        self._opensearch_password = os.getenv("OPENSEARCH-PASSWORD")

        print("Initializing OpenSearch client...")
        if not all(
            [
                self._opensearch_host,
                self._opensearch_username,
                self._opensearch_password,
            ]
        ):
            raise ValueError("Missing OpenSearch configuration in .env")

        self.client = OpenSearch(
            hosts=[{"host": self._opensearch_host, "port": 443}],
            http_auth=(self._opensearch_username, self._opensearch_password),
            use_ssl=True,
            verify_certs=True,
            ssl_show_warn=False,
            connection_class=RequestsHttpConnection,
        )
        # Check if the index exists
        if self.client.indices.exists(index=self._index_name):
            # Get document count
            doc_count = self.client.count(index=self._index_name)["count"]

            if doc_count == 0:
                self.client.indices.delete(index=self._index_name)
                print(f"Index '{self._index_name}' was empty and has been deleted.")
            else:
                print(
                    f"Index '{self._index_name}' exists and contains {doc_count} documents. Skipping deletion."
                )
        else:
            print(f"Index '{self._index_name}' does not exist.")

        # Test the connection
        try:
            info = self.client.info()
            print("Connected to OpenSearch!")
            # print(info)
        except Exception as e:
            print("Connection failed:", e)
