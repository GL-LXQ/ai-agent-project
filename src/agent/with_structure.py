from my_llm import llm
from pydantic import BaseModel, Field

class Movie(BaseModel):
  """电影详情"""
  title:str = Field(..., description="电影标题")
  year:int = Field(..., description="电影发行年份")
  director:str = Field(..., description="电影导演")
  rating: float = Field(..., description="电影评分")

model_with_structured = llm.with_structured_output(Movie)
response = model_with_structured.invoke("告诉我《夏洛特烦恼》的详细信息")
print(response)
