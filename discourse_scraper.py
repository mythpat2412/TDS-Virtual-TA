# build_vectorstore.py
import json
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# Load course content
with open("tds_scraped_content.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Split into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
course_texts = text_splitter.split_text(raw_text)
course_docs = [Document(page_content=t) for t in course_texts]

# Load discourse posts if available
discourse_docs = []
try:
    with open("discourse_posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)
        for post in posts:
            content = f"Title: {post['title']}\nDate: {post['created_at']}\nViews: {post['views']}"
            discourse_docs.append(Document(page_content=content))
except FileNotFoundError:
    print("⚠️ discourse_posts.json not found. Skipping Discourse posts.")

# Combine all docs
all_docs = course_docs + discourse_docs

# Build vectorstore
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(all_docs, embeddings)

# Save FAISS index
with open("faiss_index.pkl", "wb") as f:
    pickle.dump(db, f)

print("✅ Vectorstore built from course + discourse content and saved to faiss_index.pkl")
