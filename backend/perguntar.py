
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

CAMINHO_DB = os.path.join(os.path.dirname(__file__), "db")
MODELO_EMBEDDING = "gemini-embedding-001"
MODELO_CHAT = "gemini-3.1-flash-lite"

TEMPLATE_PROMPT = """
Responda à pergunta do usuário:
{pergunta}

Com base estritamente nestas informações:
{base_conhecimento}

Regras:
- Responda apenas com o conteúdo da resposta, em texto corrido, sem repetir a pergunta.
- Se a informação não estiver na base de conhecimento, diga que não encontrou isso nos dados.

REGRAS DE FORMATAÇÃO DE TEXTO:
1. NUNCA use formatação Markdown (não use ** para negrito, nem # para títulos, nem * para listas).
2. Para destacar o nome de um curso ou título, use LETRAS MAIÚSCULAS.
3. Separe as informações com quebras de linha duplas (parágrafos curtos) para o texto "respirar".
4. Para fazer listas, use símbolo "•" ou "->" ou numero "1 ","2" "...".
"""

_prompt = ChatPromptTemplate.from_template(TEMPLATE_PROMPT)

_modelo = ChatGoogleGenerativeAI(model=MODELO_CHAT, thinking_level="low")


def _carregar_db():
    funcao_embedding = GoogleGenerativeAIEmbeddings(
        model=MODELO_EMBEDDING,
        task_type="RETRIEVAL_QUERY",
    )
    return Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)


def responder(pergunta: str) -> str:
    db = _carregar_db()

    resultados = db.similarity_search_with_relevance_scores(pergunta, k=4)

    if len(resultados) == 0:
        return "Não consegui encontrar nenhuma informação relevante no banco de dados."

    textos_resultado = [resultado[0].page_content for resultado in resultados]
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)

    chain = _prompt | _modelo
    resposta = chain.invoke({
        "pergunta": pergunta,
        "base_conhecimento": base_conhecimento
    })

    return resposta.text

if __name__ == "__main__":
    pergunta = input("Escreva sua pergunta: ")
    print("\nAnalisando...\n")
    print("Resposta da AI:")
    print(responder(pergunta))
