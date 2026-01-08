from langchain_core.tools import BaseTool

from agent.utils.db_utils import MySqlDatabaseManger
from agent.utils.log_utils import log


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

if __name__ == "__main__":
    # 数据库连接信息
    username = "root"
    password = "123456"
    host = "127.0.0.1"
    port = 3306
    database = "bili-pro"
    # 获得数据库管理对象
    data_base_manger = MySqlDatabaseManger(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    tool = ListTablesTool(db_manager=data_base_manger)
    print(tool.invoke({}))
