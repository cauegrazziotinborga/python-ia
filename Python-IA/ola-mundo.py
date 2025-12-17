api_key = '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'

import os
os.environ['GROQ_API_KEY'] = api_key

from langchain_groq import ChatGroq

chat = ChatGroq(model='llama-3.3-70b-versatile')

resposta = chat.invoke('Liste os jogadores com mais partidas pela seleção de futebol de Ilhas Faroé')

print(resposta.content)

