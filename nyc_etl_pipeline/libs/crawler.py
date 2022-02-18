from urllib.error import HTTPError
from ..libs.config_helper import ConfigHelper
import requests
import os
import logging

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self, month, year):
        self.config = ConfigHelper("nyc_etl_pipeline").config
        self.BASE_URL = "https://s3.amazonaws.com/nyc-tlc/trip+data/"
        self.month = month
        self.year = year
        self.filename = f"yellow_tripdata_{self.year}-{self.month}.csv"
        self.url = f"{self.BASE_URL}{self.filename}"

    def download_data(self):
        if os.path.exists(os.path.join(self.config.destination_folder, self.filename)) or \
                os.path.exists(os.path.join(self.config.process_folder, self.filename)):
            logger.info("File already exist")
        else:
            try:
                logger.info(f"File not exists, downloading {self.filename}")
                data = requests.get(self.url, allow_redirects=True)
                open(os.path.join(self.config.destination_folder, self.filename), 'wb').write(data.content)
            except HTTPError as e:
                if e.code == 404:
                    logger.logging.error("File Not Found")
                else:
                    logging.error("Unexpected Error")
