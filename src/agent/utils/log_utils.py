import sys, os
from loguru import logger

#获得当前项目的绝对路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(root_dir, "logs") #存放项目日志目录的绝对路径

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# LOG_FILE = "tranlation.log" #存储日志的文件

class MyLogger:
    def __init__(self):
        # log_file_path = os.path.join(log_dir, LOG_FILE)
        self.logger = logger
        self.logger.remove()
        #输出到控制台
        self.logger.add(sys.stdout, level="DEBUG",
                        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
                        "{process.name} | " # 进程名
                        "{thread.name} | " # 线程名
                        "<cyan>{module}</cyan>.<cyan>{function}</cyan> |" # 模块名.方法名
                        ":<cyan>{line}</cyan> | " # 行号
                        "<level>{level}</level>: " # 等级
                        " <level>{message}</level>", # 日志内容
                        )
        #输出到文件
        # self.logger.add(log_file_path, level="DEBUG", encoding="UTF-8",
        #                 format="{time:YYYYMMDD HH:mm:ss} -"
        #                 "{process.name} | " # 进程名
        #                 "{thread.name} | " # 线程名
        #                 "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名
        #                 rotation="10 MB", #日志文件生成的规则 rotation="1 week"
        #                 retention=20 # 保留日志文件的规则
        # )
    def get_Logger(self):
        return self.logger
log = MyLogger().get_Logger()