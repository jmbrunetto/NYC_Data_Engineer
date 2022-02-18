import logging
from .libs.config_helper import ConfigHelper
from .libs.crawler import Crawler
from .etl import ETLProcess

logger = logging.getLogger(__name__)


class Pipeline:

    def __init__(self, args):
        self.args = args
        self.config = ConfigHelper("nyc_etl_pipeline").config

    def start(self):
        logger.info("Starting NYC ETL Pipeline")
        logger.info("Checking file requested")
        crawler = Crawler(month=self.month, year=self.year)
        crawler.download_data()
        logger.info("File Check Done, starting the load")
        process = ETLProcess()
        logger.info("Process Finished")






