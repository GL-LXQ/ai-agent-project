from langchain_openai import ChatOpenAI
from agent.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

llm = ChatOpenAI(
  model_name="deepseek-chat",
  temperature=1.3,
  api_key = DEEPSEEK_API_KEY,
  base_url=DEEPSEEK_BASE_URL,
)