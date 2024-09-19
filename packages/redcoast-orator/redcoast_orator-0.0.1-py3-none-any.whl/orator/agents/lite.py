from typing import Any, Literal, TypedDict, List
from loguru import logger

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseLanguageModel
from langgraph.graph import END, StateGraph, START

from ..chains.chitchat import ChitchatChain
from ..chains.query_router import QueryRouter
from ..chains.docs import DocsChain
from ..chains.code import CodeChain

class OratorLite:

    def __init__(
        self,
        name: str,
        paper_title: str,
        paper_fpath: str = None,
        code_fdir: str = None,
        embedding_model: Embeddings = None,
        language_model: BaseLanguageModel = None):

        self.name = name
        self.paper_title = paper_title
        self.paper_fpath = paper_fpath
        self.code_fdir = code_fdir

        self.embedding_model = embedding_model
        self.language_model = language_model

        self.query_router = QueryRouter(self.language_model)
        self.chitchat_chain = ChitchatChain(self.language_model)
        if self.paper_fpath is None:
            raise ValueError("File path is required.")
        
        self.doc_chain = DocsChain(self.paper_fpath, self.embedding_model, self.language_model)
        
        if self.code_fdir is not None:
            self.code_chain = CodeChain(self.code_fdir, embedding_model, language_model)
        else:
            self.code_chain = None
        self._build_graph()
        
    def _build_graph(self) -> None:
        class GraphState(TypedDict):
            """
            Represents the state of our graph.

            Attributes:
                question: question
                generation: LLM generation
                documents: list of documents
            """

            question: str
            language: str
            generation: str
            documents: List[str]
            code_segments: List[str]

        def retrieve_docs(state):
            logger.info("retrieve from docs")
            question = state["question"]
            language = state["language"]

            documents = self.doc_chain.retrieve_docs(question)
            return {"question": question, "language": language, "documents": documents}
        
        def retrieve_code(state):
            logger.info("retrieve from code")
            question = state["question"]
            language = state["language"]
            documents = state["documents"]

            code_segments = self.code_chain.retrieve_code(question, documents)
            return {"question": question, "language": language, "documents": documents, "code_segments": code_segments}
        
        def rag_docs(state):
            question = state["question"]
            language = state["language"]
            documents = state["documents"]

            generation = self.doc_chain.rag_generate({"question": question, "context": documents, "language": language})

            return {"documents": documents, "language": language, "question": question, "generation": generation}
        
        def rag_code(state):
            question = state["question"]
            language = state["language"]
            documents = state["documents"]
            code_segments = state["code_segments"]

            generation = self.code_chain.rag_generate(
                {"question": question, "documents": documents, "code_segments": code_segments, "language": language}
            )

            return {"documents": documents, "code_segments": code_segments, "language": language, "question": question, "generation": generation}

        def grade_documents(state):
            question = state['question']
            documents = state['documents']
            language = state["language"]

            filtered_docs = []
            for d in documents:
                score = self.doc_chain.grade_retrieval({"document": d.page_content, "question": question})
                if score == "yes":
                    filtered_docs.append(d)
                else:
                    continue

            return {"documents": filtered_docs, "language": language, "question": question}

        def grade_code_segments(state):
            question = state["question"]
            documents = state["documents"]
            code_segments = state["code_segments"]
            language = state["language"]

            filtered_codes = []
            for cs in code_segments:
                score = self.code_chain.grade_retrieval(
                    {"question": question, "code_segments": cs}
                )
                if score == "yes":
                    filtered_codes.append(cs)
                else:
                    continue
            
            return {"documents": documents, "code_segments": filtered_codes, "language": language, "question": question}
        
        def route_question(state):

            question = state["question"]
            chain = self.query_router.route_query({"question": question})

            if chain == "paper":
                return "paper"
            elif chain == "paper&code":
                return "paper&code"
            else:
                return "none"
            
        def chitchat(state):
            question = state["question"]
            documents = state["documents"]
            language = state["language"]
            generation = self.chitchat_chain.chat({"question": question, "language": language, "name": self.name, "title": self.paper_title, "context": documents})

            return {"question": question, "generation": generation, "language": language}
        
        workflow = StateGraph(GraphState)

        workflow.add_node("retrieve_docs", retrieve_docs)
        workflow.add_node("grade_documents", grade_documents)
        workflow.add_node("rag_docs", rag_docs)
        workflow.add_node("chitchat", chitchat)

        if self.code_chain:
            workflow.add_node("retrieve_code", retrieve_code)
            workflow.add_node("grade_code_segments", grade_code_segments)
            workflow.add_node("rag_code", rag_code)


        workflow.add_edge(START, "retrieve_docs")
        workflow.add_edge("retrieve_docs", "grade_documents")

        if self.code_chain is not None:
            logger.info("Build orator agent with code knowledge")
            workflow.add_conditional_edges(
                "grade_documents",
                route_question,
                {
                    "paper": "rag_docs",
                    "paper&code": "retrieve_code",
                    "none": "chitchat"
                }
            )
            workflow.add_edge("retrieve_code", "grade_code_segments")
            workflow.add_edge("grade_code_segments", "rag_code")
            workflow.add_edge("rag_code", END)
        else:
            logger.info("Build orator agent without code knowledge")
            workflow.add_conditional_edges(
                "grade_documents",
                route_question,
                {
                    "paper": "rag_docs",
                    "paper&code": "rag_docs",
                    "none": "chitchat"
                }
            )
        workflow.add_edge("chitchat", END)
        workflow.add_edge("rag_docs", END)

        self.client = workflow.compile()

    def reply(self, query, language):
        response = self.client.invoke({"question": query, "language": language})
        return response["generation"]

