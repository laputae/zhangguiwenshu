from typing import TypedDict


class DataAgentState(TypedDict):
    # 用户输入的查询
    query: str
    # 抽取的关键词
    keywords: list[str]
    # 校验SQL时出现的错误信息
    error: str
