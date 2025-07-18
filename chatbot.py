import streamlit as st
from dotenv import load_dotenv
from backend.core import Chatbot
from utils.Opensearch import OpensearchClient
from utils.Embadding import TextEmbedding
import os

# Load environment variables
load_dotenv()

# Sidebar controls
st.sidebar.title("🔧 Settings")

# Embedding model selector
embedding_model = st.sidebar.selectbox(
    "Embedding Model",
    options=["nomic-embed-text:latest", "other-model-1", "other-model-2"],
    index=0
)

# Chatbot model selector
chatbot_model = st.sidebar.selectbox(
    "Chatbot LLM Model",
    options=[
        "mistral.mixtral-8x7b-instruct-v0:1",
        "amazon.titan-text-lite-v1",
        "amazon.titan-text-express-v1"  # this one supports system messages
    ],
    index=0
)


# Button to update vector store
if st.sidebar.button("🔄 Update Vector Store"):
    st.sidebar.info("Updating vector store...")
    embedder = TextEmbedding(model=embedding_model)
    embedder.ingest_docs()
    st.sidebar.success("Vector store updated!")

# Main UI
st.title("📚 RAG Chatbot with AWS Bedrock + OpenSearch")

# Initialize OpenSearch client
opensearch_client = OpensearchClient().client
index_name = os.getenv("OPENSEARCH-INDEX-NAME")

# Check if index exists
if not opensearch_client.indices.exists(index=index_name):
    st.info(f"Index '{index_name}' does not exist. Ingesting documents...")
    embedder = TextEmbedding(model=embedding_model)
    embedder.ingest_docs()
    st.success("Documents ingested and indexed successfully.")
else:
    st.info(f"Index '{index_name}' already exists. Skipping ingestion.")

# Initialize chatbot with selected model
chatbot = Chatbot()
chatbot._embedding_model.model = embedding_model
chatbot.chat_model = chatbot_model  # You may need to pass this into BedrockLLM

# Query input
query = st.text_input("Ask a question about your documents:")

if query:
    with st.spinner("Thinking..."):
        try:
            response = chatbot.get_chatbot(query)
            st.markdown(f"**Answer:** {response['result']}")
            with st.expander("🔍 Source Documents"):
                for doc in response["source_documents"]:
                    st.markdown(f"- {doc.metadata.get('source', 'Unknown')}")
        except Exception as e:
            st.error(f"Error: {e}")
