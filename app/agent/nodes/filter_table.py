import asyncio

import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent import llm
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, TableInfoState
from app.prompt.prompt_loader import load_prompt


async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("过滤表格信息")
    query = state["query"]
    table_infos: list[TableInfoState] = state["table_infos"]
    prompt = PromptTemplate(template=load_prompt("filter_table_info"), input_variables=["query", "table_infos"])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser
    await chain.ainvoke({"query": query,
                         "table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False)})
    