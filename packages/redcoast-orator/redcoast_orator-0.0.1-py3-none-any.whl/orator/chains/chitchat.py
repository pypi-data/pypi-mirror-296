from typing import Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser

class ChitchatChain:

    def __init__(
        self, 
        language_model: BaseLanguageModel,
        chat_sys:str = None):

        self.language_model = language_model
        if chat_sys is None:
            chat_sys =  """You are a helpful AI academic speaker.
        Your name is {name}.
        You are designed to introduce the core ideas of the given paper '{title}' to the public, help readers better understand the paper, and assist them in conducting further research based on the given knowledge.
        
        You should reply in the following language: {language}. If the original paper is not in {language}, for professional terms and named entities in the paper, you need to provide both the translation of these terms and the original phrases.
        #### If the current user query is related to the given context, you should:
        1. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

        #### If the current user query is unrelated to the given context, you should:
        1. Introduce yourself.
        2. Request the user to provide a question related to the paper."""
        
        self.chat_sys = chat_sys

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", chat_sys),
                ("human", "Question: {question}\nContext: {context} ")
            ]
        )

        self.chitchat_chain = self.chat_prompt | self.language_model | StrOutputParser()

    # def invoke(self, *args: Any) -> Any:
    #     return self.chitchat_chain.invoke(*args)
    
    def chat(self, *args: Any) -> Any:
        return self.chitchat_chain.invoke(*args)