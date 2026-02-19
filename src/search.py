import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate 
from langchain.chains.combine_documents import create_stuff_documents_chain


PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

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
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

load_dotenv()
embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)

store.similarity_search("Qual é o nome da empresa?")

def search_prompt(question: str):
    
  llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

  prompt_do_rag = PromptTemplate(
      template=PROMPT_TEMPLATE,
      input_variables=["contexto", "pergunta"]
  )

  chain = create_stuff_documents_chain(llm, prompt_do_rag, document_variable_name="contexto")

  retriever = store.as_retriever(search_kwargs={"k": 10})

  if not question:
    return ""

  docs = retriever.invoke(question)

  resposta = chain.invoke({
      "contexto": docs,
      "pergunta": question
  })

  return resposta

