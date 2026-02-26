import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_core.prompts import ChatPromptTemplate

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

def build_retriever_from_url(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load()  # baixa e extrai o texto da página

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = 4
    return retriever

def answer_with_source(retriever, question: str) -> str:
    llm = ChatGroq(model=MODEL, temperature=0.5)

    relevant_docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in relevant_docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Você é o IFCBot. Responda usando APENAS o conteúdo do CONTEXTO. "
         "Se não tiver informação suficiente no contexto, diga que não encontrou no site."),
        ("user",
         "CONTEXTO:\n{context}\n\nPERGUNTA:\n{question}")
    ])

    chain = prompt | llm
    return chain.invoke({"context": context, "question": question}).content