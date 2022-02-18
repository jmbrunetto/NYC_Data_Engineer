"""nyc_elt_pipeline"""
import logging
import argparse
from .pipeline import Pipeline

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Process NYC Taxi Data.')

parser.add_argument('--month', type=str,
                    help='month to be ingested. Format (MM)')
parser.add_argument('--year', type=int,
                    help='Year to the refereed month. Format (YYYY)')
parser.add_argument('--query', type=str,
                    help='Query Historical Zones or Popular Boroughs', choices=['zones', 'boroughs'])
parser.add_argument('--pickup', type=str,
                    help='pickupPlace')


args = parser.parse_args()


if __name__ == '__main__':
    Pipeline.start(args)