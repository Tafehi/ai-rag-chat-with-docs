import os
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings

class OllamaLLM:
    def __init__(self):
        load_dotenv()
        self._model = os.getenv("MODEL_LLM")

    def get_llm(self):
        """Initialize and return the Ollama Embedding model."""
        try:
            if not self._model:
                raise ValueError("LLMMODEL environment variable is not set.")

            print(f"Using Ollama embedding model: {self._model}")
            return OllamaEmbeddings(model=self._model)

        except Exception as e:
            raise RuntimeError(f"Failed to initialize Ollama Embedding model: {e}")
