import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')

def resposta_bot(mensagens):
    mensagens_modelo = [{'system', 'Você é um assistente amigável chamado IFCBot'}]
    mensagens_modelo = mensagens_modelo = mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content

print('*** Bem-vindo ao IFCBot ***')

mensagens = []

while True:
    pergunta = input('Usuario: ')
    if pergunta.lower == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens)
    mensagens.append(('assistant', resposta))
    print(f'Bot: {resposta}')

print('Obrigado por usar o IFCBot!')
