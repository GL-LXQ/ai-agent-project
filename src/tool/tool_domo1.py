from agent.my_llm import zhipuai_client

def web_search(query: str) -> str:
    """
    互联网搜索的工具，可以搜索所有公开的信息。

    Args:
        query: 需要进行互联网查询的信息.

    Returns:
        返回搜索的结果信息，该信息是一个文本字符串。
    """
    try:
        result = zhipuai_client.web_search.web_search(
            search_engine="search_std",
            search_query=query,
        )
        if result:
            return "\n\n".join([d for d in result.search_result.content])
        return "没有搜索到任何结果"
    except Exception as e:
        print(e)
        return f"Error{e}"
