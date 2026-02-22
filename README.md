# Ingestão e Busca Semântica com LangChain e Postgres

Este projeto foi desenvolvido como parte do desafio do MBA em Engenharia de Software com IA. O objetivo é criar uma solução capaz de realizar a ingestão de documentos PDF em um banco de dados vetorial (PostgreSQL + pgVector) e permitir a realização de perguntas sobre o conteúdo do documento via interface de linha de comando (CLI).

## ✨ Funcionalidades

- **Ingestão de PDF:** Processamento e segmentação de arquivos PDF em chunks.
- **Busca Semântica:** Recuperação de informações baseada em similaridade vetorial utilizando `pgVector`.
- **RAG (Retrieval-Augmented Generation):** Respostas geradas por LLM (OpenAI ou Gemini) baseadas estritamente no conteúdo do PDF.
- **Interface CLI:** Chat interativo via terminal para consultas.

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- **Python 3.10 ou superior**
- **Docker e Docker Compose**
- **Chave de API:** OpenAI API Key ou Google AI (Gemini) API Key.

## 📂 Estrutura do Projeto

```text
├── docker-compose.yml    # Configuração do banco de dados PostgreSQL
├── requirements.txt      # Dependências do projeto
├── .env.example          # Template das variáveis de ambiente
├── src/
│   ├── ingest.py         # Script de ingestão do PDF
│   ├── search.py         # Lógica de busca semântica
│   ├── chat.py           # CLI para interação com o usuário
├── document.pdf          # PDF para ingestão (exemplo)
└── README.md             # Instruções de execução
```

## ⚙️ Configuração

### 1. Instruções para o Ambiente Virtual

Crie e ative um ambiente virtual Python:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

### 2. Instalar Dependências

Com o ambiente virtual ativo, instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

### Exemplo de Configuração (.env)

Configure as variáveis conforme sua necessidade:

```env
# Provedor de LLM (Escolha um ou ambos)
GOOGLE_API_KEY=sua_chave_do_gemini
GOOGLE_EMBEDDING_MODEL='models/embedding-001'

OPENAI_API_KEY=sua_chave_da_openai
OPENAI_EMBEDDING_MODEL='text-embedding-3-small'

# Banco de Dados
DATABASE_URL=postgresql+psycopg://langchain:langchain@localhost:6024/langchain
PG_VECTOR_COLLECTION_NAME=pdf_vectors

# Caminho do PDF
PDF_PATH=document.pdf
```

## 🛠️ Como Executar

### 1. Subir o Banco de Dados

Utilize o Docker Compose para iniciar o PostgreSQL com pgVector:

```bash
docker compose up -d
```

### 2. Executar a Ingestão do PDF

Processe o documento e armazene os embeddings no banco de dados:

```bash
python src/ingest.py
```

### 3. Iniciar o Chat (Busca)

Inicie a interface de linha de comando para fazer perguntas:

```bash
python src/chat.py
```

## 💬 Chat via CLI (Fluxo Completo)

Ao rodar o script de chat, você poderá interagir com a IA. Abaixo estão exemplos de como o sistema deve se comportar:

### Exemplo de Pergunta no Contexto
**PERGUNTA:** Qual o faturamento da Empresa SuperTechIABrazil?  
**RESPOSTA:** O faturamento foi de 10 milhões de reais.

### Exemplo de Pergunta Fora do Contexto
**PERGUNTA:** Quantos clientes temos em 2024?  
**RESPOSTA:** Não tenho informações necessárias para responder sua pergunta.

## ⚖️ Regras de Resposta

Para garantir a precisão e fidelidade ao documento, o sistema segue regras rígidas:

- **Fidelidade ao Contexto:** As respostas são geradas baseando-se **apenas** nas informações extraídas do PDF.
- **Conhecimento Externo:** O modelo está proibido de utilizar conhecimentos prévios ou externos ao documento fornecido.
- **Tratamento de Incerteza:** Caso a resposta não esteja presente no PDF, o sistema obrigatoriamente responderá: *"Não tenho informações necessárias para responder sua pergunta."*
- **Neutralidade:** O sistema não emite opiniões, interpretações ou julgamentos sobre o conteúdo.

---

## 📝 Requisitos do Desafio

- **Split:** Chunks de 1000 caracteres com overlap de 150.
- **Busca:** Recuperação dos 10 resultados mais relevantes (k=10).
- **Prompt:** Respostas estritamente baseadas no contexto fornecido, sem uso de conhecimento externo.