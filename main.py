import os
import pickle
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment")

# Define constants
VECTORSTORE_PATH = "faiss_index.pkl"
VECTORSTORE_URL = "https://your-public-link-here/faiss_index.pkl"  # 🔁 Replace with your direct link

# Download vectorstore if not already present
if not os.path.exists(VECTORSTORE_PATH):
    print("Downloading vectorstore...")
    r = requests.get(VECTORSTORE_URL)
    with open(VECTORSTORE_PATH, "wb") as f:
        f.write(r.content)

# Load vectorstore
with open(VECTORSTORE_PATH, "rb") as f:
    db = pickle.load(f)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0.7,
    max_tokens=512
)

# Define prompt
prompt_template = PromptTemplate.from_template(
    "You are a TDS Virtual TA. Use the following context to answer the question.\n\n{context}\n\nQuestion: {question}"
)

# QA chain (LangChain warning is harmless here)
qa_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=prompt_template)

# FastAPI app
app = FastAPI()

# Request schema
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "TDS Virtual TA is running. Use POST /api/ to submit questions."}

@app.post("/api/")
async def ask_question(request: QuestionRequest):
    try:
        docs = db.similarity_search(request.question, k=5)
        answer = qa_chain.run(input_documents=docs, question=request.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
