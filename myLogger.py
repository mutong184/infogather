import sys
import logging

class MyLogger:
    def __init__(self, log_file):
        # 创建日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # 创建文件处理器
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 将处理器添加到记录器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)
        print(message)  # 在控制台上显示信息

    def warning(self, message):
        self.logger.warning(message)
        print(message)  # 在控制台上显示信息

    def error(self, message):
        self.logger.error(message)
        print(message)  # 在控制台上显示信息