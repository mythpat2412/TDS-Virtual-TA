import os
import json
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# --- Load TDS course content ---
with open("tds_scraped_content.txt", "r", encoding="utf-8") as f:
    course_text = f.read()

# --- Load Discourse posts if available ---
discourse_text = ""
if os.path.exists("discourse_posts.json"):
    try:
        with open("discourse_posts.json", "r", encoding="utf-8") as f:
            discourse_data = json.load(f)
        # Join post titles and created_at for embedding
        discourse_text = "\n".join(
            f"{post['title']} ({post['created_at']})" for post in discourse_data
        )
    except Exception as e:
        print(f"⚠️ Failed to read discourse_posts.json: {e}")

# --- Combine content ---
combined_text = course_text + "\n\n" + discourse_text

# --- Split text into chunks ---
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(combined_text)

# --- Wrap in Document objects ---
documents = [Document(page_content=chunk) for chunk in chunks]

# --- Embed using HuggingFace model ---
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- Build FAISS vectorstore ---
vectorstore = FAISS.from_documents(documents, embedding_model)

# --- Save vectorstore ---
with open("faiss_index.pkl", "wb") as f:
    pickle.dump(vectorstore, f)

print("✅ Vectorstore built and saved to faiss_index.pkl")
