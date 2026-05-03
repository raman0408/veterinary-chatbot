from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def load_and_split_kb(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    raw_chunks = text.split("\n\n")
    docs = []
    for chunk in raw_chunks:
        chunk = chunk.strip()
        if chunk:
            docs.append(Document(page_content=chunk))
    
    return docs


embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

docs = load_and_split_kb("data/knowledge_base/kb.txt")


vectorstore = Chroma.from_documents(documents=docs, embedding=embedding)

def retrieve_with_scores(query: str, k: int = 1):
    results = vectorstore.similarity_search_with_score(query, k=k)

    contexts, scores = [], []
    for doc, score in results:
        contexts.append(doc.page_content)
        scores.append(score)
    return contexts, scores

