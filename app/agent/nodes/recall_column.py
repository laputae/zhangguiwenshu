from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime
from app.core.log import logger
from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.entities.column_info import ColumnInfo
from app.prompt.prompt_loader import load_prompt


async def recall_column(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    writer = runtime.stream_writer
    writer("召回字段信息")
    keywords = state["keywords"]
    query = state["query"]
    column_qdrant_repository = runtime.context["column_qdrant_repository"]
    embedding_client = runtime.context["embedding_client"]
    prompt = PromptTemplate(template=load_prompt("extend_keywords_for_column_recall"), input_variables=["query"])
    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser
    result = await chain.ainvoke({"query": query})
    keywords = set(keywords + result)
    column_info_map: dict[str, ColumnInfo] = {}
    for keyword in keywords:
        embedding = await embedding_client.aembed_query(keyword)
        current_column_infos: list[ColumnInfo] = await column_qdrant_repository.search(embedding)
        for column_info in current_column_infos:
            if column_info.id not in column_info_map:
                column_info_map[column_info.id] = column_info
    retrieved_column_infos: list[ColumnInfo] = list(column_info_map.values())
    logger.info(f"检索到字段信息，打印id: {list(column_info_map.keys())}")
    return {"retrieved_column_infos": retrieved_column_infos}
