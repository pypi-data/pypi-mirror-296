from typing import Any, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.language_models import BaseLanguageModel

class QueryRouter:

    def __init__(
        self,
        language_model: BaseLanguageModel,
        intent_sys: str = None):

        class RouteQuery(BaseModel):
            """ Route a user query to the most relevant chain"""

            relevant_chain: Literal["paper", "paper&code", "none"] = Field(
                ...,
                description="Given a user query, route it to the most relevant chain."
            )

        intent_parser = PydanticOutputParser(pydantic_object=RouteQuery)

        self.language_model = language_model

        if intent_sys is None:
            intent_sys = """You are an expert at routing a user question to the most relevant chain. The categories include: paper, paper&code, none
        - paper: The user inquires about some conceptual information (such as title, authors, the core ideas, contributions, details, exprimental results, conclusions, etc.) of the paper.
        - paper & code: The user inquires about the code implementation details of the paper.
        - none: The user's query is unrelated to the current paper or code (such as chitchating).
        
        {format_instructions}"""

        intent_route_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", intent_sys),
                ("human", "{question}")
            ]
        ).partial(format_instructions=intent_parser.get_format_instructions())

        self.question_router_chain = intent_route_prompt | self.language_model | intent_parser

    def route_query(self, *args: Any) -> Any:
        return self.question_router_chain.invoke(*args).relevant_chain