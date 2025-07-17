from fileinput import filename
import os
import streamlit as st
from dotenv import load_dotenv
from model.Bedrock import BedrockLLM
from utils.Opensearch import OpensearchClient
from utils.Embadding import TextEmbedding 




if __name__ == "__main__":
    # Initialize Bedrock LLM
    load_dotenv()
    bedrock = BedrockLLM()
    llm = bedrock.get_llm()
    print("LLM initialized successfully.")

    # Initialize OpenSearch client
    opensearch_client = OpensearchClient().client
    print("OpenSearch client initialized successfully.")

    documents_folder = os.getenv("documents_folder")
    # Initialize embedder
    embedder = TextEmbedding()
    docIngestion = embedder.ingest_docs()
    # print(f"Ingestion '{documents_folder}': {docIngestion[:5]}...")  # Show first few values














# # Initialize the model
# bedrock = BedrockLLM()
# llm = bedrock.get_llm()


# Streamlit app configuration
# st.set_page_config(page_title="Chat with Bedrock", layout="centered")
# st.title("💬 Chat with Bedrock Model")

# # Initialize session state for chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Input box for user message
# user_input = st.chat_input("Type your message here...")

# if user_input:
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # Get model response
#     response = llm(user_input)

#     # Add model response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
#     with st.chat_message("assistant"):
#         st.markdown(response)