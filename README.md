# MongoDB QA Chatbot API

This project provides a data loader for Q&A pairs and a REST API to access the data. It includes functionality to load questions and answers from a CSV file into MongoDB Atlas and provides API endpoints to query the data.

## Installation

1. Clone the repository:
bash
git clone <repository-url>
cd <repository-directory>


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit the .env file with your actual MongoDB credentials
```
env
MONGODB_USERNAME=your_username
MONGODB_PASSWORD=your_password
MONGODB_CLUSTER=your_cluster_url
MONGODB_DATABASE=chatbot
MONGODB_COLLECTION=qa_pairs


## Data Loading
# THE DATA IS ALREADT LOADED IN THE MONGODB
1. Ensure your `questions.csv` file is in the correct format:
csv
Question,Answer
"What is X?","X is..."

2. Run the data loader:
```bash
python data_loader.py
```

## API Usage

1. Start the API server:
```bash
uvicorn api:app --reload
```

2. Access the API endpoints:
```bash
http://localhost:8000/questions
```

2. The API will be available at `http://localhost:8000`

### API Endpoints

1. **Root Endpoint**
   - URL: `/`
   - Method: `GET`
   - Response: `{"message": "QA Chatbot API is running"}`

2. **Get All Questions**
   - URL: `/questions`
   - Method: `GET`
   - Response: List of all Q&A pairs
   ```json
   {
     "qa_pairs": [
       {
         "Question": "What is X?",
         "Answer": "X is..."
       }
     ]
   }
   ```

3. **Search Questions**
   - URL: `/questions/{search_term}`
   - Method: `GET`
   - Parameter: search_term (string)
   - Response: Matching Q&A pairs
   ```json
   {
     "matches": [
       {
         "Question": "What is X?",
         "Answer": "X is..."
       }
     ]
   }
   ```

4. **Get Specific Answer**
   - URL: `/answer/{exact_question}`
   - Method: `GET`
   - Parameter: exact_question (string)
   - Response: Single Q&A pair or 404 if not found

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `data_loader.py`: Loads Q&A pairs from CSV to MongoDB Atlas
- `api.py`: Defines FastAPI app and API endpoints
- `questions.csv`: Sample data for Q&A pairs
- `requirements.txt`: List of dependencies
- `.env`: Environment variables
- `README.md`: This file

## Chat Interface

1. Start the Streamlit chat interface:
```bash
streamlit run chat_interface.py
```

2. Access the chat interface in your browser:
```
http://localhost:8501
```