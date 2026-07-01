from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

FAISS_ROOT = os.getenv("FAISS_INDEX_DIR")

print("Before embeddings")
def get_embeddings():

    print("USING GEMINI EMBEDDING MODEL")

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",  #google embedding model optimized for RAG; also supports "models/textembedding-gecko-001" for general-purpose text embedding
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


def user_index_path(user_id: str, doc_id: str):

    path = os.path.join(
        FAISS_ROOT,
        str(user_id),
        str(doc_id)
    )

    os.makedirs(path, exist_ok=True)
    print("After embeddings")
    return path

  
def add_to_faiss(
    user_id: str,
    doc_id: str,
    filename: str,
    chunks: list[dict]
):

    docs = [
        Document(
            page_content=c["text"],
            metadata={
                "doc_id": doc_id,
                "filename": filename,
                "page": c["page"]
            }
        )
        for c in chunks
    ]

    vs = FAISS.from_documents(
        docs,
        get_embeddings()     
    )

    vs.save_local(
        user_index_path(user_id, doc_id)
    )
    
    print("After FAISS")
    return len(docs)


def search_faiss( 
    user_id: str,
    doc_ids: list[str],
    question: str,
    k: int = 20
):

    embeddings = get_embeddings()
  
    all_hits = []

    for doc_id in doc_ids:

        path        = user_index_path(
            user_id,
            doc_id
        )

        index_file = os.path.join(
            path,
            "index.faiss"
        )

        if not os.path.exists(index_file):
            continue

        vs = FAISS.load_local(
            path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        hits = vs.similarity_search(
            question,
            k=k
        )

        all_hits.extend(hits)
        print("After DB Save")
    return all_hits