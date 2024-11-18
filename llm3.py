#llm3.py
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def llama3(role, prompt):
    llm = Ollama(model="llama3")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", role), ("user", prompt)
    ])

    output_parser = StrOutputParser()
    chain = prompt_template | llm | output_parser

    return chain.invoke({"question": prompt})