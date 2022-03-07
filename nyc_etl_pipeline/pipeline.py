import logging
from .libs.config_helper import ConfigHelper
from .libs.crawler import Crawler
from .etl import ETLProcess

logger = logging.getLogger(__name__)


class Pipeline:

    def __init__(self, args):
        self.args = args
        self.config = ConfigHelper("nyc_etl_pipeline").config
        self.etlprocess = ETLProcess()
        self.crawler = Crawler(month=self.args.month, year=self.args.year)

    def start(self):
        logger.info("Starting NYC ETL Pipeline")
        logger.info("Checking file requested")
        self.crawler.download_data()
        logger.info("File Check Done, starting the load")
        self.etlprocess.process()
        logger.info("Process Finished")

