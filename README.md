# NYC Data Engineering Challenge

The goal for this code is to ingest the [Montlhy NYC Dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page), for this purpose, I have desingned a ETL job based on this requirements

- Load the monthly dataset into two historical tables
  - historical_zones: Contains the most popular destinations for each pick-up **zone** in terms of _number of passengers_
  - historical_boroughs: Provide the popularity for each pick-up **borough** in terms of _number of rides_
- Initial Validations about the data (_eg. Non-nulls columns_)
- Keeping only the delta on table updates (If there is no change from the last month, nothing will be added) to save disk usage
- Automatically download the dataset file based on year/month passed by parameters

## How to Run 

- Clone this repo into your local environment <br> 
```
git@github.com:jmbrunetto/NYC_Data_Engineer.git

virtualenv env python3

venv/Scritps/activate

pip install -r requirements.txt
``` 

- Update the `instance.conf` file with yours credentials
  - `destination_folder` = The folder where the dataset file will be donwloaded and readed. 
  - `process_folder` = Folder where the processed files will be stored
  - `error_folder` = Destination in case of any error on processing
  - `hostname` = Database hostname
  - `username` = Database username
  - `password` = Database password
  - `db_name`  = Database name
  - `rank_limit` = The Threshold required by the exercise (Top-K)
  - `destinations` = {"Zone" : "historical_zones", "Borough" : "historical_boroughs"}

- You can run by command line using this command `python.exe -m nyc_etl_pipeline --month 10 --year 2020`
  - Where Month = [01, 02, 03, .., 12]
  - Where Year = [2009, 2010, .., 2021]

```
(venv) PS C:\Users\BrunettJ\Projects\Drafts\NYC_Data_Engineer> python -m nyc_etl_pipeline --month 01 --year 2019
{"@timestamp":"2022-02-18 13:48:32,444","level":"INFO","message":"Starting NYC ETL Pipeline"}
{"@timestamp":"2022-02-18 13:48:32,444","level":"INFO","message":"Checking file requested"}
{"@timestamp":"2022-02-18 13:48:32,455","level":"INFO","message":"File not exists, downloading yellow_tripdata_2019-01.csv"}
{"@timestamp":"2022-02-18 13:49:27,635","level":"INFO","message":"File Check Done, starting the load"}
{"@timestamp":"2022-02-18 13:49:27,652","level":"INFO","message":"Starting yellow_tripdata_2019-01.csv ingestion"}
{"@timestamp":"2022-02-18 13:51:04,823","level":"INFO","message":"Process Finished"}
(venv) PS C:\Users\BrunettJ\Projects\Drafts\NYC_Data_Engineer> python -m nyc_etl_pipeline --month 02 --year 2019
{"@timestamp":"2022-02-18 13:51:44,632","level":"INFO","message":"Starting NYC ETL Pipeline"}
{"@timestamp":"2022-02-18 13:51:44,632","level":"INFO","message":"Checking file requested"}
{"@timestamp":"2022-02-18 13:51:44,646","level":"INFO","message":"File not exists, downloading yellow_tripdata_2019-02.csv"}
{"@timestamp":"2022-02-18 13:52:30,760","level":"INFO","message":"File Check Done, starting the load"}
{"@timestamp":"2022-02-18 13:52:30,780","level":"INFO","message":"Starting yellow_tripdata_2019-02.csv ingestion"}
{"@timestamp":"2022-02-18 13:53:53,805","level":"INFO","message":"Process Finished"}
(venv) PS C:\Users\BrunettJ\Projects\Drafts\NYC_Data_Engineer> python -m nyc_etl_pipeline --month 03 --year 2019
{"@timestamp":"2022-02-18 14:02:51,558","level":"INFO","message":"Starting NYC ETL Pipeline"}
{"@timestamp":"2022-02-18 14:02:51,559","level":"INFO","message":"Checking file requested"}
{"@timestamp":"2022-02-18 14:02:51,569","level":"INFO","message":"File not exists, downloading yellow_tripdata_2019-03.csv"}
{"@timestamp":"2022-02-18 14:03:38,664","level":"INFO","message":"File Check Done, starting the load"}
{"@timestamp":"2022-02-18 14:03:38,684","level":"INFO","message":"Starting yellow_tripdata_2019-03.csv ingestion"}
{"@timestamp":"2022-02-18 14:05:14,838","level":"INFO","message":"Process Finished"}
```

# Questions

1. The most popular destinations for each pick-up zone (top-k) in terms of the number of passengers (e.g., k=50). For instance, we want to be able to understand: Which destination was reached by the most passengers from Chinatown in September

The data source to answer this question is on historical_zones table, and can be access through the procedure `historical_zone`. I've created the procedure in order to facilitate the query on this table since the data is being kept on a delta schema.

```
CALL historical_zone('Chinatown', '2019-04-01');
```

2. The popularity of destination boroughs for each pick-up borough in terms of number of rides. The borough information can be found in the previously mentioned lookup table. As an example, we want to answer questions like: Where did the second most rides starting in Manhattan end in August 2019?

The data source to answer this question is on historical_zones table, and can be access using this query:
``
SELECT	*
FROM 	crosslend.historical_boroughs
WHERE 	month_id  = '2019-06'
AND     pick_up  = "Manhattan"
ORDER BY rank_id 
``

3. Make sure that only changed ranks are tracked in the history table.
This requirement is being done using an SQL Query to delete the duplicated tuples where the Pickup/DropOff/Rank keys are equals

4.Provide an easy way to access the currently most popular destinations per pick-up location after each new dataset was ingested.
This can be done using the procedure ``historical_zone`

```
CALL historical_zone('Chinatown', '2019-04-01');
```


5. Which steps would be necessary in order to add further information to the history
If we are talking about only add the information and not change the rank logic, this would be easily done by add new columns and setting the `process` method to gather more information. If we are planning to change the current rank loginc, we just need to increase the `send_to_destinations` and add a new destination for the news insights 

6. Argue what has to be changed/considered to create daily or yearly trends instead of a monthly aggregation?
It will not be possible use the first day of the month as an aggregator, this could be cause some issues with the validations implemented, and the way that we are ingesting. But  besides that, would be to much harder to implement a different level of aggregation. 

