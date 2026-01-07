# 在当前目录创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 停用虚拟环境
deactivate

## 前期安装
pip install langchain langchain-openai dotenv
pip install --upgrade "langgraph-cli[inmem]"
pip install -e .
pip install zai-sdk==0.2.0

# text2sql项目所需要的包
pip install sqlalchemy pymysql loguru
## 项目启动
langgraph dev

推送导origin远端的master分支
git push -u origin master