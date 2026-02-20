# Plano de Ação para Correção dos Gaps do Desafio

Este plano detalha as etapas necessárias para adequar o projeto atual 100% aos requisitos e restrições exigidos no documento `desafio.md`.

## Etapa 1: Reverter Arquitetura (Aderência à Estrutura Obrigatória)
**Objetivo:** Garantir que o projeto possua apenas os 3 arquivos Python exigidos (`ingest.py`, `search.py`, `chat.py`) dentro da pasta `src/`.
- [x] Copiar o conteúdo e as validações de ambiente de `src/config.py` de volta para o topo de `src/ingest.py` e `src/search.py`.
- [x] Copiar a inicialização do `PGVector` e `OpenAIEmbeddings` de `src/database.py` de volta para `src/ingest.py` e `src/search.py`.
- [x] Mover a variável string literal do `PROMPT_TEMPLATE` de `src/prompts/rag_prompt.py` de volta para o `src/search.py`.
- [x] Excluir com segurança os arquivos `src/config.py`, `src/database.py` e a pasta `src/prompts/`.

## Etapa 2: Adequar o Modelo de IA Exigido
**Objetivo:** Utilizar estritamente os modelos definidos nas instruções do repositório (com configuração para OpenAI).
- [x] Garantir que o `OpenAIEmbeddings` instanciado no `ingest.py` e `search.py` utilize o modelo `text-embedding-3-small`.
- [x] Garantir que o `ChatOpenAI` invocado no `search.py` utilize o modelo `gpt-5-nano` (mesmo sabendo que o modelo não existe na API comercial da OpenAI, o desafio requer exatamente essa string no código).

## Etapa 3: Renomear Variáveis do Prompt
**Objetivo:** Usar as chaves exatas de substituição pedidas no enunciado da prova.
- [x] Em `src/search.py`, modificar o `PROMPT_TEMPLATE` substituindo a chave `{contexto}` por `{resultados concatenados do banco de dados}` e a chave `{pergunta}` por `{pergunta do usuário}`.
- [x] Atualizar o `PromptTemplate(input_variables=[...])` do LangChain para refletir essas novas chaves estendidas.
- [x] Atualizar o dicionário passado ao `chain.invoke({...})` com as novas chaves para passagem de parâmetros.

## Etapa 4: Implementar o Método de Busca Específico
**Objetivo:** Substituir a engine de busca abstraída pelo método explícito `similarity_search_with_score`, para que o avaliador identifique seu uso obrigatório.
- [x] No `search.py`, remover o uso facilitado do `retriever = store.as_retriever(...)`.
- [x] Ao receber uma pergunta, implementar a busca manualmente instruindo: `resultados = store.similarity_search_with_score(question, k=10)`.
- [x] Iterar sobre os `resultados` (que retornam uma lista de tuplas contendo o documento e a nota de similaridade), filtrando e extraindo o `page_content`.
- [x] Concatenar todos os fragmentos recuperados em uma string única (formando o contexto rico) para passar de forma crua ao LLM.
