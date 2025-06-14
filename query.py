from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

def load_faiss_index():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db


def query_index(query, db, k=3):
    # Retrieve top k relevant documents for the query
    docs = db.similarity_search(query, k=k)
    return docs

if __name__ == "__main__":
    db = load_faiss_index()
    user_query = input("Enter your question: ")
    results = query_index(user_query, db)

    print("\nTop relevant results:")
    for i, doc in enumerate(results):
        print(f"Result {i+1}:\n{doc.page_content}\n---")
