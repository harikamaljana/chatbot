import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection setup
def get_database():
    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')
    database = os.getenv('MONGODB_DATABASE', 'chatbot')
    
    uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client[database]

def search_question(query: str):
    """Search for questions containing the given text"""
    try:
        db = get_database()
        collection = db[os.getenv('MONGODB_COLLECTION', 'qa_pairs')]
        results = list(collection.find(
            {"Question": {"$regex": query, "$options": "i"}},
            {'_id': 0}
        ))
        return results
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return []

# Set up Streamlit page
st.set_page_config(page_title="SAP Chatbot", page_icon="💬")

# Add clear button in the header
col1, col2 = st.columns([6,1])
with col1:
    st.title("Test Interface")
with col2:
    if st.button("Clear"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask your question about SAP"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        results = search_question(prompt)
        
        if results:
            # Display the most relevant answer
            answer = results[0]["Answer"]
            st.markdown(answer)
            
            # If there are multiple matches, show them as additional information
            if len(results) > 1:
                with st.expander("See more related answers"):
                    for idx, result in enumerate(results[1:], 1):
                        st.markdown(f"**Q{idx}:** {result['Question']}")
                        st.markdown(f"**A{idx}:** {result['Answer']}")
                        st.markdown("---")
        else:
            st.markdown("I'm sorry, I couldn't find an answer to your question. Please try rephrasing or ask something else.")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer if results else "No answer found"})

# Update sidebar
with st.sidebar:
    st.title("About")
    st.markdown("""
    This chatbot will pull data from knowledge base and answer questions.
    """) 