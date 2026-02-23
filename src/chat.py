import os
import time
from dotenv import load_dotenv
from search import search_prompt

load_dotenv()

# Códigos ANSI para cores no terminal
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def cabecalho():
    provider = os.getenv("ACTIVE_PROVIDER", "openai").lower()
    model_name = "GPT-5 Nano (OpenAI)" if provider == "openai" else "Gemini 2.5 Flash Lite (Google)"
    
    print(f"\n{CYAN}{BOLD}===================================================={RESET}")
    print(f"{CYAN}{BOLD}    Bem-vindo ao Assistente Virtual RAG-PDF    {RESET}")
    print(f"{CYAN}{BOLD}    LLM Ativa: {CYAN}{BOLD}{model_name}{RESET}")
    print(f"{CYAN}{BOLD}===================================================={RESET}")
    print(f"{YELLOW}• Digite sua pergunta sobre o documento fornecido.{RESET}")
    print(f"{YELLOW}• Para encerrar a conversa, digite '{BOLD}sair{RESET}{YELLOW}'.{RESET}\n")

def main():    
    cabecalho()

    while True:
        question = input(f"{GREEN}{BOLD}Você:{RESET} ")

        if question.lower().strip() == "sair":
            print(f"\n{CYAN}Assistente: Foi um prazer ajudar! Até logo! {RESET}\n")
            break
        
        if not question.strip():
            print(f"{YELLOW}Por favor, digite uma pergunta válida.{RESET}\n")
            continue
            
        print(f"\n{CYAN}Pensando...{RESET}")
        
        time.sleep(0.5)
        
        try:
            resposta = search_prompt(question)
            print(f"\n{BLUE}{BOLD}Resposta:{RESET} {resposta}\n")
            print(f"{CYAN}{BOLD}{'-'*52}{RESET}\n")
        except Exception as e:
            print(f"\n{YELLOW}Ops! Ocorreu um erro ao buscar a resposta: {e}{RESET}\n")

if __name__ == "__main__":
    main()