from langchain_openai import ChatOpenAI
from agent.env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
from zai import ZhipuAiClient
llm = ChatOpenAI(
  model_name="deepseek-chat",
  temperature=1.3,
  api_key = DEEPSEEK_API_KEY,
  base_url=DEEPSEEK_BASE_URL,
)

zhipuai_client = ZhipuAiClient(api_key="418ea3f347af4118ab7d528e92034d4f18ea3f347af4118ab7d528e92034d4f.EsmTkpqLA1Il10pA")
