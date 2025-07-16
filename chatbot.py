import streamlit as st
from model.Bedrock import Bedrock



if __name__ == "__main__":
    bedrock = Bedrock()
    llm = bedrock.get_llm()
    print(f"LLM initialized successfully: {llm}")














# # Initialize the model
# bedrock = Bedrock()
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