import logging
import os

log_directory = os.path.join(os.path.expanduser("~"), "yaml_plotter-logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(log_directory, "yaml_plotter.log")
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),  # 输出到文件
        logging.StreamHandler()  # 输出到控制台
    ]
)
logger = logging.getLogger(__name__)
logger.info("yaml_plotter package is imported.")

from .chart_2D import plot_2d_chart_to_file, plot_2d_chart_and_show