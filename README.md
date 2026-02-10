# 🎓 AI Chatbot for Academic & Administrative Queries

An AI-powered chatbot that answers academic and administrative questions using uploaded PDFs + general knowledge fallback.

Users can:

✅ Upload PDF documents dynamically  
✅ Ask questions about uploaded content  
✅ Get academic/general assistance  
✅ Use a clean React chat interface  
✅ Run locally or deploy to cloud  

---

## 🧠 Architecture

Frontend: React  
Backend: Flask API  
Vector Store: FAISS  
Embeddings: HuggingFace MiniLM  
LLM: Groq (Llama 3.1)  
PDF ingestion: LangChain RAG pipeline  

```
React UI → Flask API → Groq LLM + FAISS vector DB
```

---

## 📁 Project Structure

```
AI-CHATBOT/
│
├── Back-End/
│   ├── app.py
│   ├── chatbot.py
│   ├── ingest.py
│   ├── requirements.txt
│   ├── render.yaml
│   ├── vectorstore/
│   └── .env
│
└── Front-End/chatbot-ui/
    ├── src/
    ├── public/
    ├── package.json
```

---

## ⚙️ Backend Setup

### 1. Create virtual environment

```bash
cd Back-End
python -m venv venv
venv\Scripts\activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create `.env` file

Inside `Back-End/.env`

```
GROQ_API_KEY=your_groq_api_key_here
```

👉 Generate key: https://console.groq.com/keys

---

### 4. Run backend

```bash
python app.py
```

Backend runs at:

```
http://localhost:5000
```

---

## 🎨 Frontend Setup

```bash
cd Front-End/chatbot-ui
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 📄 Upload PDFs

Use the upload button in UI.

Uploaded PDFs are:

- chunked
- embedded
- stored in FAISS vector database
- queried during chat

Each new upload rebuilds the vector DB.

---

## 💬 Chat Logic

1. If question matches PDF context → RAG answer
2. If no match → Groq general assistant fallback

So it behaves like:

> smart document assistant + academic AI tutor

---

## 🚀 Deployment Options

### Backend (Render / Railway / Fly.io)

Deploy Flask API using:

- Render
- Railway
- Fly.io
- AWS
- Azure

Use `render.yaml` for Render deployment.

---

### Frontend

Deploy React UI on:

- Vercel
- Netlify
- GitHub Pages

Set backend URL in frontend config.

---

## 🔒 Security Notes

Never commit:

```
.env
venv/
vectorstore/
node_modules/
```

Use `.gitignore`.

Rotate API keys if leaked.

---

## 🧪 Local Testing

Test API:

```
http://localhost:5000/test
```

Chat endpoint:

```
POST /chat
```

Upload endpoint:

```
POST /upload
```

---

## 📌 Features

✔ Dynamic PDF ingestion  
✔ Retrieval-Augmented Generation  
✔ Academic assistant mode  
✔ General fallback AI  
✔ React chat UI  
✔ Groq ultra-fast inference  
✔ Deploy-ready structure  

---

## 🧠 Future Improvements

- Multi-document memory
- chat history persistence
- authentication
- admin dashboard
- PDF tagging
- streaming responses
- role-based access

---

## 👩‍💻 Author

Built for academic AI assistance and campus automation.

---

## 📜 License

MIT License
