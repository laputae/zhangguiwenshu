from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.agent.llm import llm
from app.entities.value_info import ValueInfo
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


async def recall_value(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("召回字段取值")
    query=state["query"]
    keywords=state["keywords"]
    value_es_repository=runtime.context["value_es_repository"]

    prompt = PromptTemplate(template=load_prompt("extend_keywords_for_value_recall"), input_variables=[])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser
    result = await chain.ainvoke({"query": query})
    keywords = set(keywords + result)

    value_infos_map:dict[str, ValueInfo] = {}
    for keyword in keywords:
        current_value_infos:list[ValueInfo]=await value_es_repository.search(keyword)
        for current_value_info in current_value_infos:
            if current_value_info.id not in value_infos_map:
                value_infos_map[current_value_info.id]=current_value_info
    retrieved_value_infos:list[ValueInfo]=list(value_infos_map.values())
    logger.info(f"检索到字段取值，打印key: {list(value_infos_map.keys())}")
    return {"retrieved_value_infos": retrieved_value_infos}