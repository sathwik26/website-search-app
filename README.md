Website Content Search – React + Flask + Pinecone

A Single Page Application (SPA) where users enter a website URL + search query, and the system returns the top 10 relevant HTML content chunks (max 500 tokens each) using semantic search with embeddings & Pinecone vector DB.

Features

-> Input website URL & search keyword
->Fetch & clean HTML (no JavaScript pages)
->Tokenize into 500-token chunks
->Embed using SentenceTransformer
->Store/search vectors using Pinecone
->Show top 10 relevant chunks in UI

contents in each file 
/backend:
app.py- main server
/utils/parser.py - HTML parsing and chunking
/utils/vector_store.py- pinecone integration
requirements.txt-python dependencies

/frontend:
App.js- React UI
api.js-Axios API
App.css  - styling

Setup Instructions
1️.Backend Setup (Flask + Pinecone)
cd backend
pip install -r requirements.txt
python -m nltk.downloader punkt

Create .env:

PINECONE_API_KEY=your_api_key
PINECONE_ENVIRONMENT=us-east-1
INDEX_NAME=website-search-index

Run backend:

python app.py

Runs at → http://127.0.0.1:5000

2. Frontend Setup (React)
cd frontend
npm install
npm start

Runs at → http://localhost:3000

->Vector DB Setup – Pinecone

Create free account → https://pinecone.io

Copy API key & environment → Add to .env

Index auto-created in code if not found

