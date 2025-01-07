# MongoDB QA Chatbot API

This project provides a data loader for Q&A pairs and a REST API to access the data. It includes functionality to load questions and answers from a CSV file into MongoDB Atlas and provides API endpoints to query the data.

## Installation

1. Clone the repository:
bash
git clone https://github.com/harikamaljana/chatbot.git
cd chatbot


2. Install dependencies:
```bash
pip install -r requirements.txt
```

## API Usage

1. Start the API server:
```bash
uvicorn api:app --reload
```

## Chat Interface

1. Start the Streamlit chat interface:
```bash
streamlit run chat_interface.py
```

2. Access the chat interface in your browser:
```
http://localhost:8501
```
