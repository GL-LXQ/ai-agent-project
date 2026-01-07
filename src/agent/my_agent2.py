from langchain.agents import create_agent
from agent.my_llm import llm
# from agent.tool.tool_demo1 import web_search
from tool import WebSearchTool

web_search_tool =  WebSearchTool()

agent = create_agent(
  llm,
  tools=[web_search_tool],
  system_prompt="你是一个智能助手，尽可能的调用工具回答用户的问题。",
)