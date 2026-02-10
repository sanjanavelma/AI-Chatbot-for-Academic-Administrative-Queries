import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# load .env
load_dotenv(".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print("DEBUG ENV:", GROQ_API_KEY)

if GROQ_API_KEY is None or GROQ_API_KEY.strip() == "":
    raise RuntimeError("GROQ_API_KEY not found in .env file")

VECTORSTORE_PATH = "vectorstore"

# embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# LLM
llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.3,
    groq_api_key=GROQ_API_KEY,
)

# RAG prompt
rag_prompt = ChatPromptTemplate.from_template("""
You are an academic assistant chatbot.

Answer using ONLY the context below.
If the context does not contain the answer, say:
"I don't find this in the uploaded documents."

Context:
{context}

Question:
{question}
""")

# general fallback prompt
general_prompt = ChatPromptTemplate.from_template("""
You are an academic & administrative assistant.
Answer clearly and professionally.

Question:
{question}
""")

def ask_bot(question):
    if not question:
        return "Please ask a question."

    # if no uploaded docs → general chat
    if not os.path.exists(VECTORSTORE_PATH):
        chain = general_prompt | llm | StrOutputParser()
        return chain.invoke({"question": question})

    # load vector DB
    db = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(question)

    # if no relevant docs → general chat
    if not docs:
        chain = general_prompt | llm | StrOutputParser()
        return chain.invoke({"question": question})

    # RAG chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    answer = rag_chain.invoke(question)

    # fallback if RAG fails
    if "don't find this" in answer.lower():
        chain = general_prompt | llm | StrOutputParser()
        return chain.invoke({"question": question})

    return answer
