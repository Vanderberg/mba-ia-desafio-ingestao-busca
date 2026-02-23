import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{resultados concatenados do banco de dados}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta do usuário}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

provider = os.getenv("ACTIVE_PROVIDER", "openai").lower()

if provider == "openai":
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0.5)
elif provider == "gemini":
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.5)
else:
    raise ValueError(f"Provedor {provider} não suportado.")

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)

prompt_do_rag = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["resultados concatenados do banco de dados", "pergunta do usuário"]
)

chain = prompt_do_rag | llm | StrOutputParser()

def search_prompt(question: str):

  if not question or not question.strip():
    raise ValueError("Question inválida.")

  # Usando o método exigido pelo desafio
  # resultados_crus = store.similarity_search_with_score(question, k=10)  
  resultados_crus = store.similarity_search_with_score(question.strip(), k=10)
  
  textos_recuperados = []
  for resultado in resultados_crus:
      # Dependendo da versão, o 'resultado' pode ser (Document, score) ou (str, score),
      # e a propriedade pode se chamar page_content. Tentamos todas falhas de forma segura.
      doc = resultado[0] if isinstance(resultado, (tuple, list)) else resultado
      
      if hasattr(doc, "page_content"):
          textos_recuperados.append(str(doc.page_content))
      else:
          textos_recuperados.append(str(doc))
          
  contexto_concatenado = "\n".join(textos_recuperados)

  resposta = chain.invoke({
      "resultados concatenados do banco de dados": contexto_concatenado,
      "pergunta do usuário": question
  })

  return resposta
