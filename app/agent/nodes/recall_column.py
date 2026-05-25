import asyncio

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.prompt.prompt_loader import load_prompt
from app.agent.llm import llm


async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("召回字段信息")
    keywords = state["keywords"]
    query = state["query"]
    column_qdrant_repository = runtime.context["column_qdrant_repository"]
    embedding_client = runtime.context["embedding_client"]
    prompt = PromptTemplate(template=load_prompt("extend_keywords_for_column_recall"), input_variables=[])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser
    result = chain.ainvoke({"query": query})
    keywords = set(keywords + result)
