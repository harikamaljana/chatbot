import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

def load_qa_to_mongodb():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get MongoDB credentials from environment variables
    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')
    database = os.getenv('MONGODB_DATABASE', 'chatbot')
    collection_name = os.getenv('MONGODB_COLLECTION', 'qa_pairs')
    
    # Construct the MongoDB URI
    uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
        
        # Select database and collection
        db = client[database]
        collection = db[collection_name]
        
        # Read the CSV file
        csv_path = 'questions.csv'
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Could not find {csv_path}")
        
        # Load data from CSV
        df = pd.read_csv(csv_path)
        
        # Convert DataFrame to list of dictionaries
        qa_pairs = df.to_dict('records')
        
        # Drop existing collection to avoid duplicates
        collection.drop()
        
        # Insert the QA pairs
        result = collection.insert_many(qa_pairs)
        print(f"Successfully inserted {len(result.inserted_ids)} QA pairs into MongoDB")
        
    except Exception as e:
        print(f"Connection error: {str(e)}")
        print("Please verify:")
        print("1. Your MongoDB Atlas username and password are correct")
        print("2. Your IP address is whitelisted in MongoDB Atlas")
        print("3. The connection string format is correct")
        raise
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    load_qa_to_mongodb() 