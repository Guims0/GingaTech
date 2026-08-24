
import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PASTA_BASE = os.path.join(os.path.dirname(__file__), "data")
CAMINHO_DB = os.path.join(os.path.dirname(__file__), "db")

MODELO_EMBEDDING = "gemini-embedding-001"


def criar_db():
    print("Iniciando o processamento dos documentos...")
    documentos = carregar_documentos()

    if not documentos:
        print(f"Nenhum documento encontrado na pasta '{PASTA_BASE}'.")
        return

    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)
    print(f"Sucesso! Banco criado em '{CAMINHO_DB}' com {len(chunks)} fragmentos.")


def carregar_documentos():
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    return carregador.load()


def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )
    return separador_documentos.split_documents(documentos)


def vetorizar_chunks(chunks):

    funcao_embedding = GoogleGenerativeAIEmbeddings(
        model=MODELO_EMBEDDING,
        task_type="RETRIEVAL_DOCUMENT",
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=funcao_embedding,
        persist_directory=CAMINHO_DB
    )


if __name__ == "__main__":
    criar_db()
