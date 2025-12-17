import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')

template = ChatPromptTemplate.from_messages(
    [
        ('system', 'Você é um assistente que sempre responde com piadas'),
        ('user', 'Traduza {expressao} para a lingua {lingua}')
    ]
)

chain = template | chat

resposta = chain.invoke({'expressao': 'tchê', 'lingua': 'inglesa'})

print(resposta.content)
