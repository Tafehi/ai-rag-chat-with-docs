import os
from dotenv import load_dotenv
from opensearchpy import OpenSearch


class OpensearchClient:
    """
    A class to manage the OpenSearch client connection and vector operations.
    """

    def __init__(self):
        load_dotenv()
        self._opensearch_host = os.getenv("OPENSEARCH_HOST")
        self._opensearch_username = os.getenv("OPENSEARCH_USERNAME")
        self._opensearch_password = os.getenv("OPENSEARCH_PASSWORD")

        print("Initializing OpenSearch client...")
        if not all([self._opensearch_host, self._opensearch_username, self._opensearch_password]):
            raise ValueError("Missing OpenSearch configuration in .env")

        self.client = OpenSearch(
            hosts=[{"host": self._opensearch_host, "port": 443}],
            http_auth=(self._opensearch_username, self._opensearch_password),
            use_ssl=True,
            verify_certs=True,
            ssl_show_warn=False
        )

        # Test the connection
        try:
            info = self.client.info()
            print("Connected to OpenSearch!")
            print(info)
        except Exception as e:
            print("Connection failed:", e)


if __name__ == "__main__":
    try:
        opensearch_client = OpensearchClient()
        print("OpenSearch client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize OpenSearch client: {e}")


