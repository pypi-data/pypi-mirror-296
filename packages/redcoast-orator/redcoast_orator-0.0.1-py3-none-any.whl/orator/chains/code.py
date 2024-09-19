from typing import Any, List, Literal
# from git import Repo
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from orator.vectorstores.chroma import OratorChroma

class CodeChain:

    def __init__(
        self,
        code_fdir: str,
        embedding_model: Embeddings,
        language_model: BaseLanguageModel,
        chunks_size: int = 2000,
        chunks_overlap: int = 20,
        transform_usr: str = None,
        rag_usr: str = None,
        relevance_grade_sys: str = None
    ):
        
        self.embedding_model = embedding_model
        self.language_model = language_model
        
        code_loader = GenericLoader.from_filesystem(
            code_fdir,
            glob = "**/*",
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=2)
        )
        documents = code_loader.load()

        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=chunks_size, chunk_overlap=chunks_overlap
        )
        code_splits = code_splitter.split_documents(documents)

        vectorstore = OratorChroma.from_documents(
            documents=code_splits,
            collection_name="code_collection",
            embedding=embedding_model
        )

        self.code_retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 8}
        )

        # chain 1: query transform
        if transform_usr is None:
            transform_usr = """Given the above conversation, generate a search query to look up code segments relevant to the conversation.
            
        Raw Question: {question} 
        Relevant Docs: {documents} 
        Search Query: """
        
        transform_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", transform_usr)
            ]
        )

        self.transform_chain = transform_prompt | self.language_model | StrOutputParser()

        if rag_usr is None:
            rag_usr = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        You should reply in the following language: {language}. If the original paper is not in {language}, for professional terms and named entities in the paper, you need to provide both the translation of these terms and the original phrases.

        Question: {question} 
        Relevant Docs: {documents}
        Relevant Code Segments: {code_segments} 
        Answer: """
            
        rag_prompt = ChatPromptTemplate.from_messages([
            ("human", rag_usr)
        ])

        # Post-processing
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.format_docs = format_docs

        self.rag_chain = rag_prompt | self.language_model | StrOutputParser()

        # chain 3: retrieval grader
        class GradeCodeSegments(BaseModel):
            """ Binary score for relevance check on retrieved code segment."""
            binary_score: Literal["yes", "no"] = Field(
                ...,
                description="Code segment is relevant to the question, 'yes' or 'no'."
            )

        grade_parser = PydanticOutputParser(pydantic_object=GradeCodeSegments)

        if relevance_grade_sys is None:
            relevance_grade_sys = """You are a grader assessing relevance of a retrieved code segment to a user question.
        If the code segment contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
        It does not need to be a stringent test. The goal is to filter out erroneous retrievals.
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
        
        {format_instructions}"""
            
        relevance_grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", relevance_grade_sys),
                ("human", "Retrieved_code_segment: \n\n{code_segments} \n\n User question: {question}")
            ]
        ).partial(format_instructions=grade_parser.get_format_instructions())

        self.retrieval_grader = relevance_grade_prompt | self.language_model | grade_parser
    
    def retrieve_code(self, question: str, documents: List[str]) -> Any:
        actual_query = self.transform_chain.invoke(
            {"question": question, "documents": documents}
        )
        return self.code_retriever.invoke(actual_query)
    
    def rag_generate(self, *kwargs: Any) -> Any:
        return self.rag_chain.invoke(*kwargs)
    
    def grade_retrieval(self, *kwargs: Any) -> Any:
        return self.retrieval_grader.invoke(*kwargs).binary_score