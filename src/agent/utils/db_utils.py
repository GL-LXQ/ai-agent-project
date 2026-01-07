from typing import List, Optional

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from agent.utils.log_utils import log
class MySqlDatabaseManger:
    """数据库链接管理器，负责数据库连接和基本操作"""
    def __init__(self, connection_string: str):
        """
        初始化数据库连接
        Args:
            connection_string:MySql连接字符串, 格式为 mysql+pymysql://username:password@host:port/database
        """
        self.engine = create_engine(connection_string, pool_size=5, pool_recycle=3600)

    def get_table_names(self):
        """获取数据库中所有表名"""
        try:
            inspector = inspect(self.engine)  # 数据库映射对象
            return inspector.get_table_names()
        except Exception as e:
            log.debug(e)
            raise ValueError(f"获取表名失败：{str(e)}")

    def get_tables_name_with_comments(self) -> List[dict]:
        """
        获取数据库中所有表名和对应的描述
        """
        try:
            query = text("""
                     SELECT TABLE_NAME, TABLE_COMMENT
                     FROM INFORMATION_SCHEMA.TABLES
                     WHERE TABLE_SCHEMA = DATABASE()
                       AND TABLE_TYPE = 'BASE TABLE'
                     ORDER BY TABLE_NAME
                     """)
            with self.engine.connect() as connection:
                result = connection.execute(query)
                #将结果转为字典列表，便于后续处理
                table_info = [{"table_name": row[0], "table_comment": row[1]} for row in result]
                return table_info
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表名机器描述信息失败:{str(e)}")

    def get_table_schema(self, table_names: Optional[List[str]]):
        """
        获取表结构
        Args:
            table_names: 表名列表,如果为None，则获取所有表
        """
        try:
            inspector = inspect(self.engine)
            schema_info = []
            tables_to_process = table_names if table_names else self.get_table_names()

            for table_name in tables_to_process:
                # 获取表结构
                columns = inspector.get_columns(table_name)
                pk_constraint = inspector.get_pk_constraint(table_name)
                primary_keys = pk_constraint["constrained_columns"] if pk_constraint else []
                foreign_keys = inspector.get_foreign_keys(table_name)
                indexes = inspector.get_indexes(table_name)

                # 构建表模式描述
                table_schema = f"表名: {table_name}\n"
                table_schema += "列信息: \n"

                for column in columns:
                    pk_indicator = " (主键)" if column["name"] in primary_keys else ""
                    # 获取字段注释，如果不存在则显示无注释
                    comment = column.get("comment", "无注释")
                    table_schema += f" -{column["name"]}: {str(column["type"])}{pk_indicator} [注释: {comment}]\n"

                if foreign_keys:
                    table_schema += "外键约束: \n"
                    for foreign_key in foreign_keys:
                        table_schema += f" -{foreign_key["constraint_columns"]} -> {foreign_keys["referred_table"]}.{foreign_keys["referred_column"]}"

                if indexes:
                    table_schema += "索引信息: \n"
                    for index in indexes:
                        if not index["name"].startswith("sqlite_"):
                            table_schema += f" -{index['name']}: {index['column_names']} ({'唯一' if index.get('unique') else ''})\n"

                schema_info.append(table_schema)
            return "\n".join(schema_info) if schema_info else "未找到匹配的表"
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表结构失败：{str(e)}")


if __name__ == "__main__":
    #配置数据库连接信息
    username = "root"
    password = "123456"
    host = "127.0.0.1"
    port = 3306
    database = "bili-pro"
    #获得数据库管理对象
    data_base_manger = MySqlDatabaseManger(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4")
    #获得数据库表名
    print(data_base_manger.get_table_names())
    print(data_base_manger.get_tables_name_with_comments())
    print(data_base_manger.get_table_schema(data_base_manger.get_table_names()))

