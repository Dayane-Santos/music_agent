from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools import tool

# Uploads and vectorizes the internal policy manual
loader = PyPDFLoader("data/policy_manual.pdf")
documents = loader.load_and_split()
vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

@tool
def search_policy_manual(doubt: str) -> str:
    """
    Check the store's internal policies: returns, warranty, shipping rules, payment methods, and operating hours.
    """
    docs = retriever.invoke(doubt)
    return "\n\n".join([doc.page_content for doc in docs])