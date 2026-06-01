import yaml
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def correct_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("修正SQL")

    table_infos = state["table_infos"]
    metric_infos = state["metric_infos"]
    data_info = state["date_info"]
    db_info = state["db_info"]
    query = state["query"]
    sql = state["sql"]
    error = state["error"]

    prompt = PromptTemplate(template=load_prompt("correct_sql"),
                            input_variables=["table_infos", "metric_infos", "date_info", "db_info", "query", "sql",
                                             "error"])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    result = await chain.ainvoke({"table_infos": yaml.dump(table_infos, allow_unicode=True, sort_keys=False),
                                  "metric_infos": yaml.dump(metric_infos, allow_unicode=True, sort_keys=False),
                                  "date_info": yaml.dump(data_info, allow_unicode=True, sort_keys=False),
                                  "db_info": yaml.dump(db_info, allow_unicode=True, sort_keys=False),
                                  "query": query,
                                  "sql": sql,
                                  "error": error})
    logger.info(f"修正后的SQL是: {result}")
