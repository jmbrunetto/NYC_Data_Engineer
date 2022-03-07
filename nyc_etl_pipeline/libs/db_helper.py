from sqlalchemy import create_engine
from ..libs.config_helper import ConfigHelper
import logging

logger = logging.getLogger(__name__)


class DbConn:

    def __init__(self):
        self.config = ConfigHelper("nyc_etl_pipeline").config
        self.hostname = self.config.hostname
        self.username = self.config.username
        self.password = self.config.password
        self.db_name = self.config.db_name

    def create_conn(self):
        try:
            conn_str = f"mysql+pymysql://{self.username}:{self.password}@{self.hostname}:3306/{self.db_name}"
            engine = create_engine(conn_str)
        except Exception as e:
            logger.error(f"Failed to connect to db with error: {e}")
        return engine

    @staticmethod
    def close_conn(engine):
        engine.dispose()

    def write_to_db(self, df, table_name):
        engine = self.create_conn()
        try:
            df.to_sql(table_name, engine, if_exists='append', index=False)
            if table_name == "historical_zones":
                self.remove_duplicate_ranks(engine,table_name)
        except Exception as e:
            logger.error(f"Failed to connect to db with error: {e}")
            raise e
        finally:
            self.close_conn(engine)

    def remove_duplicate_ranks(self, engine, table):
        #Need to add the month filter on line 47 to avoid compare with older data
        sql_query = f"""DELETE   p1
                        FROM     {table} AS p1 
                        CROSS JOIN ( SELECT	 pick_up, drop_off , rank_id, max(month_id) month_id 
                                     FROM 	 {table}
                                     WHERE   month_id = {table} 
                                     GROUP   BY 1, 2, 3
                                     HAVING  COUNT(1) > 1
                                   ) AS p2
                        USING (pick_up, drop_off, rank_id, month_id);
                    """
        self.execute_query(engine, sql_query)

    def execute_query(self, engine, query):
        try:
            engine.execute(query)
        except Exception as e:
            logger.error(f"Failed to delete duplicates ranks: {e}")



