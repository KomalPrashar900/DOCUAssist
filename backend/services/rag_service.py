# backend/services/rag_service.py
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain_core.prompts import PromptTemplate
# from services.embed_service import add_to_faiss, search_faiss
import os
from dotenv import load_dotenv

load_dotenv()

"GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY")

"""CHUNK_SIZE    = int(os.getenv('CHUNK_SIZE'))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP'))
LLM_MODEL     = os.getenv('LLM_MODEL')
print(LLM_MODEL)

# Prompt that prevents hallucination
RAG_PROMPT = PromptTemplate(
    input_variables=['context', 'question'],
    template=You are a helpful document assistant. Answer the
question using ONLY the information from the context below.
If the answer is not clearly present, respond:
'I could not find relevant information in your documents.'
Do not mention document names in the answer.

Context:
{context}

Question: {question}
Answer:
)

def chunk_pages(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
        separators=['\n\n', '\n', '. ', ' ', '']
    )
    chunks = []
    for page in pages:
        for text in splitter.split_text(page['text']):
            chunks.append({'text': text, 'page': page['page']})
    return chunks

def ingest_document(user_id: str, doc_id: str,
                     filename: str, pages: list) -> int:
    chunks = chunk_pages(pages)
    return add_to_faiss(user_id, doc_id, filename, chunks)

def answer_question(user_id: str, doc_ids: list[str],
                     question: str) -> dict:
    # Step 1: Retrieve relevant chunks
    relevant = search_faiss(user_id, doc_ids, question)

    if not relevant:
        return {
            'answer': 'I could not find relevant information in your documents.',
            'sources': []
        }

    # Step 2: Build context string
    context = '\n\n---\n\n'.join(c.page_content for c in relevant)
    sources = [
        {'filename': c.metadata['filename'],
         'page': c.metadata['page'],
         'preview': c.page_content[:120] + '...'}
        for c in relevant
    ]

    # Step 3: Generate answer with LLM
    llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
   )
    prompt = RAG_PROMPT.format(context=context, question=question)
    answer = llm.invoke(prompt).content

    return {'answer': answer, 'sources': sources}"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

from services.embed_service import (
    add_to_faiss,
    search_faiss
)

from dotenv import load_dotenv
import os

load_dotenv()                                                                                                                    

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
LLM_MODEL = os.getenv("LLM_MODEL")


RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful document assistant. 

Answer the question using ONLY the information
from the context below.

If the answer is not clearly present, respond:

'I could not find relevant information in your documents.'

Do not mention document names in the answer.

Context:
{context}

Question:
{question}

Answer:
"""
)


def chunk_pages(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for page in pages:
        texts = splitter.split_text(
            page["text"]
        )

        for text in texts:
            chunks.append({
                "text": text,
                "page": page["page"]
            })

    return chunks


def ingest_document(
    user_id: str,
    doc_id: str,
    filename: str,
    pages: list
) -> int:

    # optional: limit pages for large PDFs
    pages = pages[:50]

    chunks = chunk_pages(pages)

    # limit chunks to avoid Gemini free-tier quota
    MAX_CHUNKS = 100

    if len(chunks) > MAX_CHUNKS:
        print(
            f"Large document detected. "
            f"Limiting chunks to {MAX_CHUNKS}"
        )

        chunks = chunks[:MAX_CHUNKS]

    return add_to_faiss(
        user_id,
        doc_id,
        filename,
        chunks
    )

def answer_question(
    user_id: str,
    doc_ids: list[str],
    question: str
) -> dict:

    relevant = search_faiss(
        user_id,
        doc_ids,
        question
    ) 

    if not relevant:
        return {
            "answer":
                "I could not find relevant information in your documents.",
            "sources": []
        }

    context = "\n\n---\n\n".join(
        c.page_content for c in relevant
    )

    sources = [
        {
            "filename":
                c.metadata["filename"],
            "page":
                c.metadata["page"],
            "preview":
                c.page_content[:120] + "..."
        }
        for c in relevant
    ]

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0,
        google_api_key=os.getenv(
            "GOOGLE_API_KEY"
        )
    )

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    answer = llm.invoke(prompt).content

    return {
        "answer": answer,
        "sources": sources
    }