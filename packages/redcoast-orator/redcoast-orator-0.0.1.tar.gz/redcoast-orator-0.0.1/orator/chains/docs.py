from typing import Literal, Any
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.language_models import BaseLanguageModel
from langchain_community.document_loaders.generic import GenericLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from orator.vectorstores.chroma import OratorChroma

class DocsChain:

    def __init__(
        self,
        doc_fpath: str,
        embedding_model: Embeddings,
        language_model: BaseLanguageModel,
        chunks_size: int = 2000,
        chunks_overlap: int = 20,
        relevance_grade_sys: str = None,
        rag_usr: str = None,
        hallucination_grade_sys: str = None,
        answer_grade_sys: str = None,
        rewrite_sys: str = None):

        self.embedding_model = embedding_model
        self.language_model = language_model

        # Document Retriever
        paper_loader = GenericLoader.from_filesystem(
            doc_fpath,
            glob="**/*",
            suffixes=[".pdf"]
        )
        documents = paper_loader.load()

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunks_size, chunk_overlap=chunks_overlap
        )
        doc_splits = text_splitter.split_documents(documents)

        vectorstore = OratorChroma.from_documents(
            documents=doc_splits,
            collection_name="docs_collection",
            embedding=embedding_model
        )

        self.doc_retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8}
        )

        # chain 1: retrieval grader
        class GradeDocuments(BaseModel):
            """ Binary score for relevance check on retrieved documents."""

            binary_score: Literal["yes", "no"] = Field(
                ...,
                description="Documents are relevant to the question, 'yes' or 'no'."
            )

        grade_parser = PydanticOutputParser(pydantic_object=GradeDocuments)

        if relevance_grade_sys is None:
            relevance_grade_sys = """You are a grader assessing relevance of a retrieved document to a user question.
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
        
        {format_instructions}"""

        relevance_grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", relevance_grade_sys),
                ("human", "Retrieved_document: \n\n{document} \n\n User question: {question}")
            ]
        ).partial(format_instructions=grade_parser.get_format_instructions())

        self.retrieval_grader = relevance_grade_prompt | self.language_model | grade_parser

        # chain 2: rag generator
        if rag_usr is None:
            rag_usr = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        You should reply in the following language: {language}. If the original paper is not in {language}, for professional terms and named entities in the paper, you need to provide both the translation of these terms and the original phrases.

        Question: {question} 
        Context: {context} 
        Answer: """
        rag_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", rag_usr)
            ]
        )

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.format_docs = format_docs
        
        self.rag_chain = rag_prompt | self.language_model | StrOutputParser()

        # chain 3: hallucination grader
        class GradeHallucinations(BaseModel):
            """ Binary score for hallucination check on generated answer."""

            binary_score: Literal["yes", "no"] = Field(
                ...,
                description="Answer contains hallucinations, 'yes' or 'no'."
            )

        hallucination_parser = PydanticOutputParser(pydantic_object=GradeHallucinations)

        if hallucination_grade_sys is None:
            hallucination_grade_sys =  """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
        Give a binary score 'yes' or 'no'. 'yes' means that the answer is grounded in / supported by the set of facts.
        
        {format_instructions}"""

        hallucination_grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", hallucination_grade_sys),
                ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
            ]
        ).partial(format_instructions=hallucination_parser.get_format_instructions())

        self.hallucination_grader = hallucination_grade_prompt | self.language_model | hallucination_parser

        # chain 4: answer grader
        class GradeAnswer(BaseModel):
            """ Binary score for answer quality check."""

            binary_score: Literal["yes", "no"] = Field(
                ...,
                description="Answer addresses the question, 'yes' or 'no'"
            )

        answer_parser = PydanticOutputParser(pydantic_object=GradeAnswer)

        if answer_grade_sys is None:
            answer_grade_sys = """You are a grader assessing whether an answer addresses / resolves a question \n 
        Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.
        
        {format_instructions}"""

        answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", answer_grade_sys),
                ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
            ]
        ).partial(format_instructions=answer_parser.get_format_instructions())

        self.answer_grader = answer_prompt | self.language_model | answer_parser

        # chain 5: question re-writer

        if rewrite_sys is None:
            rewrite_sys = """You a question re-writer that converts an input question to a better version that is optimized 
        for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""

        rewrite_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", rewrite_sys),
                ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question.")
            ]
        )

        self.question_rewriter = rewrite_prompt | self.language_model | StrOutputParser()

    def retrieve_docs(self, question: str) -> Any:
        return self.doc_retriever.invoke(question)
    
    def rag_generate(self, *kwargs: Any) -> Any:
        return self.rag_chain.invoke(*kwargs)
    
    def grade_retrieval(self, *kwargs: Any) -> Any:
        return self.retrieval_grader.invoke(*kwargs).binary_score
    
    def rewrite_query(self, *kwargs: Any) -> str:
        return self.question_rewriter.invoke(*kwargs)
    
    def grade_hallucination(self, *kwargs: Any) -> str:
        return self.hallucination_grader.invoke(*kwargs).binary_score
    
    def grade_answer(self, *kwargs: Any) -> str:
        return self.answer_grader.invoke(*kwargs).binary_score