mapper = {
    'VendorID': "object",
    'tpep_pickup_datetime': "string",
    'tpep_dropoff_datetime': "string",
    'passenger_count': float,
    'trip_distance': float,
    'RatecodeID': float,
    'store_and_fwd_flag': "string",
    'PULocationID': float,
    'DOLocationID': float,
    'payment_type': float,
    'fare_amount': float,
    'extra': float,
    'mta_tax': float,
    'tip_amount': float,
    'tolls_amount': float,
    'improvement_surcharge': float,
    'total_amount': float,
    'congestion_surcharge': float
}

parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']