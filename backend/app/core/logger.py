"""
日志配置模块
使用 Loguru 实现异步日志处理
"""
import sys
from pathlib import Path
from loguru import logger

# 日志目录
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def setup_logger():
    """配置日志格式和输出"""
    # 移除默认处理器
    logger.remove()

    # 控制台输出格式
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )

    # 文件输出格式
    logger.add(
        LOG_DIR / "acg_blog_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="00:00",  # 每天零点轮换
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        encoding="utf-8",
    )

    return logger


# 初始化日志
app_logger = setup_logger()
