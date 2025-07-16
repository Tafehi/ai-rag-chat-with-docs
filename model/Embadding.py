import os
import json
from langchain.embeddings.base import Embeddings
from dotenv import load_dotenv
from model.Ollama import OllamaLLM
from model.Bedrock import Bedrock

class TitanTextLiteEmbeddings(Embeddings):
    def __init__(self):
        load_dotenv()
        self._llm_model = os.getenv("MODEL_LLM")

        if "titan" in self._llm_model.lower():
            print(f"Using Bedrock model: {self._llm_model}")
            self.client = Bedrock().get_llm()
            self.provider = "bedrock"
        else:
            print(f"Using Ollama model: {self._llm_model}")
            self.client = OllamaLLM().get_llm()
            self.provider = "ollama"

    def embed_documents(self, texts):
        return [self._embed(text) for text in texts]

    def embed_query(self, text):
        return self._embed(text)

    def _embed(self, text):
        if self.provider == "bedrock":
            response = self.client.invoke_model(
                modelId=self._llm_model,
                body=json.dumps({"inputText": text}),
                contentType="application/json",
            )
            result = json.loads(response["body"].read())
            return result["embedding"]
        elif self.provider == "ollama":
            return self.client.embed_query(text)
        else:
            raise ValueError("Unsupported provider")

