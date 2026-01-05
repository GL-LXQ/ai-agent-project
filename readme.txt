# 在当前目录创建虚拟环境
python -m venv myenv

# 激活虚拟环境
.\myenv\Scripts\Activate.ps1

# 停用虚拟环境
deactivate

## 前期安装
pip install langchain langchain-openai dotenv
pip install --upgrade "langgraph-cli[inmem]"
pip install -e .
## 项目启动
langgraph dev