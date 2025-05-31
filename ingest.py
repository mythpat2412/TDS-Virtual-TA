import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / ".env")

# Check for API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please set it in the .env file.")
print(f"OPENAI_API_KEY loaded: {api_key[:8]}...")

# Import LangChain libraries AFTER loading env variables
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Build path to your text file
data_file = project_root / "data" / "tds_course.txt"
if not data_file.exists():
    raise FileNotFoundError(f"❌ Data file not found: {data_file}")

# Load documents
loader = TextLoader(str(data_file), encoding="utf-8")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Create OpenAI embeddings object (uses your API key from env automatically)
embeddings = OpenAIEmbeddings()

# Create FAISS vector store from docs + embeddings
db = FAISS.from_documents(docs, embeddings)

# Save vectorstore locally
db.save_local(str(project_root / "vectorstore"))

print("✅ Ingestion complete. Vector store saved to 'vectorstore/'")
