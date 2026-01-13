
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, create_model
from agent.utils.db_utils import MySqlDatabaseManger
from agent.utils.log_utils import log
from typing import List, Optional, Any


class ListTablesTool(BaseTool):
    name: str = "sql_db_list_tables"
    description: str = "列出MySql数据库中所有的表名及其对应的描述信息，当需要了解数据库中有多少表和表的信息时调用。"
    db_manager: MySqlDatabaseManger

    def _run(self):
        try:
            tables_info = self.db_manager.get_tables_name_with_comments()
            # print(tables_info)
            result = f"数据库中共有 {len(tables_info)} 个表：\n "
            for index, table_info in enumerate(tables_info):
                index = index + 1
                table_name = table_info["table_name"]
                table_comment = table_info["table_comment"]
                if not table_comment or table_comment.isspace():
                    table_comment = "暂无描述"
                result += f"{index}.表名:{table_name}\n"
                result += f"   描述:{table_comment}\n\n"
            return result
        except Exception as e:
            log.debug(e)
            return f"列出表时出错：{str(e)}"

    async def _async_run(self):
        """异步执行"""
        return self._run()

class TableSchemaTool(BaseTool):
    name: str="sql_db_schema"
    description: str="获取MySql数据库中指定表的详细模式信息，包括列定义、主键、外键等。输入应为表名列表，以获取所有表信息"
    db_manager: MySqlDatabaseManger

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 告知大模型，调用此工具需要什么参数
        self.args_schema = create_model("TableSchemaToolArgs", table_names=(List[str], Field(..., description="表名的列表")))

    def _run(self, table_names: List[str]) -> str:
        """"
        返回表结构信息
        """
        try:
            schema_info = self.db_manager.get_table_schema(table_names)
            return schema_info if schema_info else "未找到匹配的表"
        except Exception as e:
            log.debug(f"获取表模式信息时出错:{e}")
            return f"获取表模式信息时出错:{e}"
    async def _arun(self, table_names: List[str]) -> str:
        """异步执行"""
        return self._run(table_names)


class SQLQueryCheckerTool(BaseTool):
    """检查SQL查询语法"""
    name: str = "sql_db_query_checker"
    description: str = "检查SQL查询语句的语法是否正确，提供验证反馈。输入应为要检查的SQL查询语句"
    db_manager: MySqlDatabaseManger

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model(
            "SQLQueryCheckerArgs",
            query=(str, Field(..., description="需要进行检查的SQL语句"))
        )

    def _run(self, query: str) -> str:
        """执行工具逻辑"""
        try:
            result = self.db_manager.validate_query(query)
            return result
        except Exception as e:
            log.debug(f"检查sql查询语句时出错:{e}")
            return f"检查sql查询语句时出错:{e}"

    async def _arun(self, query) -> str:
        """异步执行"""
        return self._run(query)

class SQLQueryTool(BaseTool):
    """执行SQL查询"""
    name: str = "sql_db_query"
    description: str = "在MySQL数据库上执行安全的SELECT查询并返回结果，输入应为有效的SQL SELECT查询语句"
    db_manager: MySqlDatabaseManger

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args_schema = create_model(
            "SQLQueryToolArgs",
            query = (str, Field(..., description="有效的SQL SELECT查询语句"))
        )

    def _run(self, query: str) -> str:
        try:
            result = self.db_manager.execute_query(query)
            return result
        except Exception as e:
            log.debug(f"执行sql查询语句时出错:{e}")
            return f"执行sql查询语句时出错:{e}"

    async def _arun(self, query) -> str:
        """异步执行"""
        return self._run(query)


if __name__ == "__main__":
    # 数据库连接信息
    username = "root"
    password = "123456"
    host = "127.0.0.1"
    port = 3306
    database = "ai"
    # 获得数据库管理对象
    data_base_manger = MySqlDatabaseManger(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    tool = SQLQueryTool(db_manager=data_base_manger)
    print(tool.invoke({"query": "SELECT count(*) FROM USER"}))
