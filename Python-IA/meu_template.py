from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages(
    [('user', 'Traduza (expressão) para a lingua (lingua)')]
)

resultado = template.invoke({'expressao': 'legal', 'lingua': 'inglesa'})

print(resultado)
