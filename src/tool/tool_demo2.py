from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, create_model

from agent.my_llm import zhipuai_client


class WebSearchTool(BaseTool):
    name: str = "web_search2"

    description: str = "使用这个工具可以进行网络搜索"

    def __init__(self):
        super().__init__()
        self.args_schema = create_model("searchInput", query=(str, Field(..., description="需要进行互联网查询的信息")))

    def _run(self, query: str) -> str:
        try:
            result = zhipuai_client.web_search.web_search(
                search_engine="search_std",
                search_query=query,
            )
            if result:
                return "\n\n".join([d.content for d in result.search_result])
            return "没有搜索到任何结果"
        except Exception as e:
            print(e)
            return f"Error{e}"
