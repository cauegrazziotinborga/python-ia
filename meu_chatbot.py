import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not API_KEY:
    raise RuntimeError("Faltou GROQ_API_KEY no .env")

chat = ChatGroq(model=MODEL, temperature=0.7)

SYSTEM = ("system", "Você é um assistente amigável chamado IFCBot. Responda de forma clara e objetiva.")

def main():
    print("*** Bem-vindo ao IFCBot ***")
    print("Digite /sair para encerrar.\n")

    mensagens = [SYSTEM]

    while True:
        pergunta = input("Usuário: ").strip()
        if not pergunta:
            continue
        if pergunta.lower() in ["/sair", "sair", "/exit", "x"]:
            break

        mensagens.append(("user", pergunta))

        # manda a lista toda (histórico) pro modelo
        resposta = chat.invoke(mensagens).content

        mensagens.append(("assistant", resposta))
        print(f"\nBot: {resposta}\n")

    print("Obrigado por usar o IFCBot!")

if __name__ == "__main__":
    main()