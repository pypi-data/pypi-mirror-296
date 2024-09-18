import sys
import time
from loguru import logger as log
from pathlib import Path

LEVEL = "INFO"

project_path = Path.cwd()
log_path = Path(project_path, "logs")
t = time.strftime("%Y-%m-%d")

log.remove(0)
log.add(sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green> | "  # 颜色>时间
               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
               "<cyan>[{line}]</cyan> | "  # 行号
               "<level>{level}[{thread.name}]</level>： "  # 等级 # 线程名
               "<level>{message}</level>",  # 日志内容
        level=LEVEL,
        )
log.add(sink=f"{log_path}/info_{t}.log",
        format="<green>{time:YYYY-MM-DD HH:mm:ss:SSS}</green> | "  # 颜色>时间
               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
               "<cyan>[{line}]</cyan> | "  # 行号
               "<level>{level}[{thread.name}]</level>： "  # 等级 # 线程名
               "<level>{message}</level>",  # 日志内容
        level='INFO', rotation='00:00', encoding="utf-8", enqueue=True,
        retention="2 days")

logger = log
