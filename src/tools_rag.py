from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.tools import tool

load_dotenv()

_retriever = None

def init_rag():
    global _retriever
    if _retriever is None:
        loader = PyPDFLoader("data/políticas_da_loja.pdf")
        documents = loader.load_and_split()
        embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        vectorstore = Chroma.from_documents(documents, embeddings)
        _retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return _retriever

@tool
def search_policy_manual(duvida: str) -> str:
    """Consulta as políticas internas da loja: devoluções, garantia, regras de frete, formas de pagamento e horários de funcionamento."""
    retriever = init_rag()
    docs = retriever.invoke(duvida)
    return "\n\n".join([d.page_content for d in docs])