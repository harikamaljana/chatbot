import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pandas as pd

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

# Set up Streamlit page
st.set_page_config(page_title="Q&A Database", page_icon="📚")
st.title("Knowledge Base")

try:
    # Get database connection
    db = get_database()
    collection = db[os.getenv('MONGODB_COLLECTION', 'qa_pairs')]
    
    # Fetch all Q&A pairs
    qa_pairs = list(collection.find({}, {'_id': 0}))
    
    if qa_pairs:
        # Convert to DataFrame for better display
        df = pd.DataFrame(qa_pairs)
        
        # Add search functionality
        search_term = st.text_input("Search in questions and answers:")
        
        if search_term:
            # Filter DataFrame based on search term
            mask = (df['Question'].str.contains(search_term, case=False)) | \
                  (df['Answer'].str.contains(search_term, case=False))
            filtered_df = df[mask]
        else:
            filtered_df = df
        
        # Display total count
        st.write(f"Total Number of Q&A: {len(filtered_df)}")
        
        # Display as expandable cards
        for idx, row in filtered_df.iterrows():
            with st.expander(f"Q: {row['Question']}"):
                st.write("**Question:**")
                st.write(row['Question'])
                st.write("**Answer:**")
                st.write(row['Answer'])
        
    else:
        st.warning("No Q&A pairs found in the database.")
        
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")

# Add sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This page displays all questions and answers in the knowledge base.
    """) 