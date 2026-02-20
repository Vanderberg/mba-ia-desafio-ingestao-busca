from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate 
from database import get_vector_store 
from langchain.chains.combine_documents import create_stuff_documents_chain

from prompts.rag_prompt import PROMPT_TEMPLATE

store = get_vector_store()

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.5)

prompt_do_rag = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["contexto", "pergunta"]
)

chain = create_stuff_documents_chain(llm, prompt_do_rag, document_variable_name="contexto")
retriever = store.as_retriever(search_kwargs={"k": 10})

def search_prompt(question: str):

  if not question:
    return ""

  docs = retriever.invoke(question)

  resposta = chain.invoke({
      "contexto": docs,
      "pergunta": question
  })

  return resposta

