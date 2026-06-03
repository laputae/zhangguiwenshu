import asyncio

import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.llm import llm
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState, TableInfoState
from app.prompt.prompt_loader import load_prompt
from app.core.log import logger

async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer({"type": "progress", "step": "过滤表格信息", "status": "running"})

    try:
        query = state["query"]
        table_infos: list[TableInfoState] = state["table_infos"]
        prompt = PromptTemplate(template=load_prompt("filter_table_info"), input_variables=["query", "table_infos"])
        output_parser = JsonOutputParser()
        chain = prompt | llm | output_parser
        result = await chain.ainvoke({"query": query,
                                      "table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False)})
        filter_table_infos: list[TableInfoState] = []
        for table_info in table_infos:
            if table_info["name"] in result:
                table_info["columns"] = [column_info for column_info in table_info["columns"] if
                                         column_info["name"] in result[table_info["name"]]]
                filter_table_infos.append(table_info)
        logger.info(f"过滤之后的表信息: {filter_table_infos}")
        writer({"type": "progress", "step": "过滤表格信息", "status": "success"})
        return {"table_infos": filter_table_infos}
    except Exception as e:
        logger.error(f"过滤表格信息失败: {e}")
        writer({"type": "progress", "step": "过滤表格信息", "status": "error"})
        raise
