import os
import re
import sys
import logging
from functools import wraps
from datetime import datetime
import shutil


def normalize_path(path):
    """
    确保文件夹路径统一以斜线结尾
    """
    # 首先使用 normpath 规范化路径
    normalized_path = os.path.normpath(path)
    
    # 检查路径是否以斜线结尾，如果不是，则添加斜线
    if not normalized_path.endswith(os.sep):
        normalized_path += os.sep
    
    return normalized_path

def save_dict(input_dict, file_name):
     """
     将字典保存为 py 文件（中的 data 字典）。

     提供一种完全 Pythonic 的配置写入读取方式。
     """
     dict_str = "data = {\n"
     for key, value in input_dict.items():
         key_str = f"'{key}'" if isinstance(key, str) else str(key)
         value_str = f"'{value}'" if isinstance(value, str) else str(value)
         dict_str += f"      {key_str}: {value_str},\n"
     dict_str += "}\n"

     if os.path.dirname(file_name) and not os.path.exists(os.path.dirname(file_name)):
         # 如果指定了不存在的目录就创建目录
         os.makedirs(os.path.dirname(file_name))

     # 写入到文件
     with open(file_name, 'w+', encoding="utf-8") as file:
         file.write(dict_str)

def load_dict(file_path):
    """
    从指定路径中读取 python 字典数据
    """
    if not file_path.endswith(".py"):
        raise ValueError("The path string does not end in '.py'!")
    else:
        # 移除结尾的 ".py"
        file_path = file_path[:-3]
    
    file_name = os.path.basename(file_path)
    dir_path  = os.path.dirname(file_path)

    sys.path.append(dir_path)  # 替换为你的实际路径
    exec(f"import {file_name}  ;global data  ;data = {file_name}.data")
    return data

    
    

class LittleLog:
    def __init__(self, log_path="", config_path=""):
        """
        初始化LittleLog实例，设置默认值并创建日志记录器
        """
        if log_path:
            self._outputs = OutputList(self, [log_path])
        else:
            self._outputs = OutputList(self)
        self._level = "debug"
        self._max_file_size = 2     # MB
        self._max_files = 10
        self._terminal = True
        self._logger = None
        self._today = datetime.now().strftime("%Y-%m-%d")
        self.config_path = config_path    # 若指定，则将从该路径读取并保存日志系统配置文件
        self._setup_logger()


    @property
    def outputs(self):
        """
        获取日志输出路径列表
        """
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        print("触发了outputs_setter, value: ", value)
        """
        设置日志输出路径列表，并更新日志处理器
        """
        if not isinstance(value, list):
            raise ValueError("'outputs' must be a list!")
        self._outputs = OutputList(self, value)
        self._update_handlers()

        if self.config_path:
            self.save_config()

    @property
    def level(self):
        """
        获取当前日志级别
        """
        return self._level

    @level.setter
    def level(self, value):
        """
        设置日志级别，并更新日志记录器的级别
        """
        if value not in ["debug", "info", "warning", "error", "critical"]:
            raise ValueError(f"Invalid logger level <{value}>!")
        self._level = value
        self._logger.setLevel(getattr(logging, value.upper()))
        self._update_handlers()

        if self.config_path:
            self.save_config()

    @property
    def max_file_size(self):
        """
        获取单个日志文件的最大大小（MB）
        """
        return self._max_file_size

    @max_file_size.setter
    def max_file_size(self, value):
        """
        设置单个日志文件的最大大小（MB）
        """
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("'max_file_size' must be a positive integer!")
        self._max_file_size = value

        self._update_handlers()

        if self.config_path:
            self.save_config()

    @property
    def max_files(self):
        """
        获取最大日志文件数量
        """
        return self._max_files

    @max_files.setter
    def max_files(self, value):
        """
        设置最大日志文件数量
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError("'max_files' must be a positive integer!")
        self._max_files = value

        self._update_handlers()

        if self.config_path:
            self.save_config()

    @property
    def terminal(self):
        """
        获取是否启用控制台输出
        """
        return self._terminal

    @terminal.setter
    def terminal(self, value):
        """
        设置是否启用控制台输出
        """
        if not isinstance(value, bool):
            raise ValueError("'terminal' must be Boolean!")
        self._terminal = value

        self._update_handlers()

        if self.config_path:
            self.save_config()

    def _setup_logger(self):
        """
        设置日志记录器，创建处理器
        """

        # 配置日志
        self._logger = logging.getLogger("LittleLog")
        self._logger.setLevel(logging.DEBUG)
        self._update_handlers()

        # 如果开启了配置文件 - 读取&建立配置
        if self.config_path:
            # 如果配置了工程目录，就从配置文件读取配置。
            print("目录是：", normalize_path(self.config_path) + "ezlog_config.py")
            if os.path.exists(normalize_path(self.config_path) + "ezlog_config.py"):
                print("存在，加载")
                self.load_config()
            else:
                print("不存在，重新创建")
                self.save_config()

            self._update_handlers() # debug 测试

    def _update_handlers(self):
        """
        更新日志输出器
        ========================

        作用是更新输出目的地（不同的文件、控制台）。

        logging 模块内置的文件滚动功能不足以实现 LittleLog 的滚动需求，因此我们自己来实现。

        :说明:
            1. handler 是日志输出器，指定日志输出格式与目的地（特定文件或控制台）
            2. _logger 是日志总控，可以包含多个 handler，以不同配置向多个目的地输出日志。
        
        """
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)

        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d - %(levelname)s\n%(message)s\n', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        for output in self._outputs:
            # 文件日志 - 包含 更新文件&删除文件 操作
            os.makedirs(output, exist_ok=True)
            handler = logging.FileHandler(self._get_log_file_path(output), encoding='utf-8')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        if self.terminal:
            # 控制台日志
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def _get_log_file_path(self, output_dir):
        """
        获取新日志文件的路径，如果当前文件已满则创建新文件
        """
         
        today = datetime.now().strftime("%Y-%m-%d")

        file_counter = self._get_file_counter(output_dir)     # 获取当前日志编号
        
        if today != self._today:
            # 换日，文件序号从头开始递增。
            file_counter = 1
            self._today = today

        file_name = f"log_{today}_{file_counter}.txt"
        file_path = os.path.join(output_dir, file_name)

        if os.path.exists(file_path):
            if os.path.getsize(file_path) < self._max_file_size * 1024 * 1024:
                return file_path

            # 如果最新日志文件大小超出设定上限
            else:   
                file_counter += 1

                file_name = f"log_{today}_{file_counter}.txt"
                file_path = os.path.join(output_dir, file_name)
                
                # 如果所有文件都已满，删除最旧的文件并返回新文件路径
                self._remove_oldest_file(output_dir)
                return file_path
        else:
            return file_path

    def _remove_oldest_file(self, output_dir):
        """
        删除最旧的日志文件，当达到最大文件数量限制时
        
        （注意是按最后修改时间删除，不是按编号删除。）
        """
        files = sorted([f for f in os.listdir(output_dir) if f.startswith("log_")], 
                       key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        if len(files) >= self._max_files:
            os.remove(os.path.join(output_dir, files[0]))

    def _get_file_counter(self, directory):
        """
        找出当前日期的日志中的最大序号（找出当前处理日志的序号）
        """
        today = datetime.now().strftime("%Y-%m-%d")

        pattern = re.compile(f"log_{today}" + r"_(\d+)\.txt$")

        max_num = 1
        max_file = None
        # 遍历目录中的所有文件
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if match:
                # 将匹配到的数字转换为整数
                num = int(match.group(1))
                # 如果找到更大的数字，则更新 max_num 和 max_file
                if num > max_num:
                    max_num = num
                    max_file = filename

        return max_num

    def add_output(self, output):
        """
        添加新的日志输出路径
        """
        if output not in self._outputs:
            self._outputs.append(output)
            self._update_handlers()

    def remove_output(self, output):
        """
        移除指定的日志输出路径
        """
        if output in self._outputs:
            self._outputs.remove(output)
            self._update_handlers()

    def debug(self, message):
        """
        记录调试级别的日志
        """
        self._update_handlers()        
        self._logger.debug(message)

    def info(self, message):
        """
        记录信息级别的日志
        """
        self._update_handlers()
        self._logger.info(message)

    def warning(self, message):
        """
        记录警告级别的日志
        """
        self._update_handlers()
        self._logger.warning(message)

    def error(self, message):
        """
        记录错误级别的日志
        """
        self._update_handlers()
        self._logger.error(message)

    def critical(self, message):
        """
        记录严重错误级别的日志
        """
        self._update_handlers()
        self._logger.critical(message)

    def log_decorator(self, func):
        """
        日志装饰器，用于记录函数的执行情况
        =============================================

        仅仅是调用 5 个标准方法来输出日志，没有创建新的日志输出方式。
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.debug(f"Function Start: {func.__name__}")
            try:
                result = func(*args, **kwargs)
                self.debug(f"Function complete: {func.__name__}")
                return result
            except Exception as e:
                self.error(f"Function execution error: {func.__name__}, Messages: {str(e)}")
                raise
        return wrapper

    def save_config(self, path=""):
        """
        保存日志全局配置到 path 路径
        """
        if not path:
            path = self.config_path
            
        path = normalize_path(path)     # 确保文件夹路径统一以斜线结尾

        data = {
            "outputs": self.outputs,
            "level": self.level,
            "max_file_size": self.max_file_size,
            "max_files": self.max_files,
            "terminal": self.terminal
        }
        save_dict(data, f"{path}ezlog_config.py")

    def load_config(self, path=""):
        """
        从 path 路径中读取日志全局配置
        """
        if not path:
            path = self.config_path
            
        path = normalize_path(path)     # 确保文件夹路径统一以斜线结尾
        file_path = path + "ezlog_config.py"

        if not os.path.exists(file_path):
            raise Exception(
                f"Log system configuration file {file_path} does not exist, " +
                "please call save_config() method to create the configuration file!"
            )

        # 读取配置文件
        config = load_dict(file_path)

        # 更新配置 - 从内部变量进行更新，避免触发【日志输出目标自动重新配置】【配置文件自动记录】
        self._outputs = OutputList(self, config["outputs"])
        self._level = config["level"]
        self._max_file_size = config["max_file_size"]
        self._max_files = config["max_files"]
        self._terminal = config["terminal"]


class OutputList(list):
    """
    自定义列表类，在修改时自动更新日志处理器
    """
    def __init__(self, easy_log, *args):
        """
        初始化OutputList实例
        """
        super().__init__(*args)
        self.easy_log = easy_log

    def append(self, item):
        """
        添加新项并更新日志处理器
        """
        if item in self:
            print(f"LittleLog warning: An existing path was added: <{item}>")
            return 1
        else:
            print(f"LittleLog debug: Path added successfully: <{item}>")
        super().append(item)
        self = OutputList(self.easy_log, list(set(self)))
        self.easy_log._update_handlers()

    def remove(self, item):
        """
        移除项并更新日志处理器
        """
        super().remove(item)
        self.easy_log._update_handlers()

    def extend(self, items):
        """
        扩展列表并更新日志处理器
        """
        super().extend(items)
        self.easy_log._update_handlers()


def new(log_path="", config_path=""):
    return LittleLog(log_path=log_path, config_path=config_path)

# 创建LittleLog实例
logger = LittleLog()

# 函数日志装饰器
debugger = logger.log_decorator



