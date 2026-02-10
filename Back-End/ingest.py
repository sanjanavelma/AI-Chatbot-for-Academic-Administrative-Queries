import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTORSTORE_PATH = "vectorstore"

# embeddings (load once)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def ingest_single_file(filepath):
    print(f"\n📄 Ingesting new file: {filepath}")

    # ✅ wipe old DB safely
    if os.path.exists(VECTORSTORE_PATH):
        print("🧹 Clearing old vectorstore...")
        shutil.rmtree(VECTORSTORE_PATH)

    # load pdf
    loader = PyPDFLoader(filepath)
    documents = loader.load()

    if not documents:
        raise RuntimeError("❌ PDF loaded but no text found.")

    print(f"✅ Loaded {len(documents)} pages")

    # split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    texts = splitter.split_documents(documents)

    print(f"✂️ Split into {len(texts)} chunks")

    # build vector DB
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(VECTORSTORE_PATH)

    print("✅ New clean vectorstore built!\n")
