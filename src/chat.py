from search import search_prompt

def main():    
    
    print("Faça sua pergunta (digite 'sair' para encerrar):\n")

    while True:
        question = input("Usuário: ")

        if question.lower() == "sair":
            break
        
        resposta = search_prompt(question)
        print("Resposta:", resposta)

if __name__ == "__main__":
    main()