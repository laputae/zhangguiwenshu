import asyncio

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent import llm
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.prompt.prompt_loader import load_prompt


async def filter_table(state:DataAgentState,runtime:Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("过滤表格信息")

    prompt = PromptTemplate(template=load_prompt("filter_table_info"), input_variables=[])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser
    