from .libs.config_helper import ConfigHelper
from .libs.db_helper import DbConn
from .model import yellow_dataset
import os
import shutil
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ETLProcess:

    def __init__(self):
        self.config = ConfigHelper("nyc_etl_pipeline").config
        self.db_conn = DbConn()
        self.process()

    def process(self):
        input_file_path = self.config.destination_folder
        if os.path.exists(input_file_path):
            for file in os.listdir(input_file_path):
                if file[0:1] != '.':
                    logger.info(f"Starting {file} ingestion")
                    try:
                        df = pd.read_csv(f"{input_file_path}\{file}",
                                         dtype=yellow_dataset.mapper,
                                         parse_dates=yellow_dataset.parse_dates)
                        valid_df = self.validate(df, file)
                        # Selecting only the columns needed
                        valid_df = valid_df[["month_id", "PULocationID", "DOLocationID", "passenger_count"]]

                        self.send_to_destinations(valid_df, self.config.destinations)

                        shutil.move(f"{input_file_path}\{file}", f"{self.config.process_folder}\{file}")
                    except Exception as e:
                        logger.error(f"it was not possible to load {file} due to {e}")
                        shutil.move(f"{input_file_path}\{file}", f"{self.config.error_folder}\{file}")

    def validate(self, df, filename):
        return_df = df.dropna(subset=['PULocationID', 'DOLocationID', "tpep_pickup_datetime"])
        return_df["month_id"] = pd.to_datetime(return_df["tpep_pickup_datetime"]).dt.strftime("%Y-%m")
        final_df = return_df.loc[(return_df['month_id'] == str.split(filename, '_')[2][0:7])]
        return final_df

    def create_ranking_qtd_passenger_or_trips(self, df, method):
        # Creating the Aggregation to use Rank
        # With method = sum we are agg the qty of user who travel
        # With method = coutn we are agg the qty of trips
        work_df = df.groupby(["pick_up", "drop_off", "month_id"]). \
            agg({"passenger_count": method}). \
            reset_index()
        # Creating Rank based on N of passengers
        work_df["rank_id"] = work_df.groupby(["pick_up", "month_id"])["passenger_count"] \
            .rank("dense", ascending=False).astype(int)
        # Limiting the Rank based on Top-k
        work_df.drop(work_df[work_df['rank_id'] > self.config.rank_limit].index, inplace=True)
        work_df.drop(columns=["passenger_count"], inplace=True)
        return work_df



    def send_to_destinations(self, df, destinations):
        try:
            for destination, table in destinations.items():
                pre_df = self.lookup_zone_ids(df, destination)
                if destination == "Zone":
                    result_df = self.create_ranking_qtd_passenger_or_trips(pre_df, "sum")
                else:
                    result_df = self.create_ranking_qtd_passenger_or_trips(pre_df, "count")
                # Resolving the IDs to Zones/Borough Names
                self.db_conn.write_to_db(result_df, table)
        except Exception as e:
            logger.error(f"It was not possible to lookup the Locations - {e}")

    def lookup_zone_ids(self, df, destination):
        lookup_df = pd.read_csv("etc/lookup/taxi_zone_lookup.csv")
        merged_df = df.merge(lookup_df[["LocationID", f"{destination}"]], left_on="PULocationID", right_on="LocationID")
        merged_df.drop(columns=["LocationID"], inplace=True)
        merged_df.rename(columns={f"{destination}": "pick_up"}, inplace=True)
        merged_df = merged_df.merge(lookup_df[["LocationID", f"{destination}"]], left_on="DOLocationID", right_on="LocationID")
        merged_df.drop(columns=["LocationID", "PULocationID", "DOLocationID"], inplace=True)
        merged_df.rename(columns={f"{destination}": "drop_off"}, inplace=True)
        return merged_df


