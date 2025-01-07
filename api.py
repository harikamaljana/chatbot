from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="QA Chatbot API")

# MongoDB connection setup
def get_database():
    username = os.getenv('MONGODB_USERNAME')
    password = os.getenv('MONGODB_PASSWORD')
    cluster = os.getenv('MONGODB_CLUSTER')
    database = os.getenv('MONGODB_DATABASE', 'chatbot')
    
    uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client[database]

@app.get("/")
async def root():
    return {"message": "QA Chatbot API is running"}

@app.get("/questions")
async def get_all_questions():
    """Get all questions and answers from the database"""
    try:
        db = get_database()
        collection = db[os.getenv('MONGODB_COLLECTION', 'qa_pairs')]
        qa_pairs = list(collection.find({}, {'_id': 0}))
        return {"qa_pairs": qa_pairs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/questions/{question}")
async def search_question(question: str):
    """Search for questions containing the given text"""
    try:
        db = get_database()
        collection = db[os.getenv('MONGODB_COLLECTION', 'qa_pairs')]
        results = list(collection.find(
            {"Question": {"$regex": question, "$options": "i"}},
            {'_id': 0}
        ))
        if not results:
            raise HTTPException(status_code=404, detail="No matching questions found")
        return {"matches": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/answer/{question}")
async def get_answer(question: str):
    """Get the exact answer for a specific question"""
    try:
        db = get_database()
        collection = db[os.getenv('MONGODB_COLLECTION', 'qa_pairs')]
        result = collection.find_one(
            {"Question": {"$regex": f"^{question}$", "$options": "i"}},
            {'_id': 0}
        )
        if not result:
            raise HTTPException(status_code=404, detail="Question not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 