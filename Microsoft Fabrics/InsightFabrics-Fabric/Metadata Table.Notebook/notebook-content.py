# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "baf1fc42-d907-4f03-a097-08b602d8a0c8",
# META       "default_lakehouse_name": "LhInsightFabric",
# META       "default_lakehouse_workspace_id": "bc7938fc-605d-41ac-ac76-fb76a0c0cac4",
# META       "known_lakehouses": [
# META         {
# META           "id": "baf1fc42-d907-4f03-a097-08b602d8a0c8"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC CREATE TABLE IF NOT EXISTS table_metadata (
# MAGIC     table_name STRING,
# MAGIC     layer STRING,
# MAGIC     grain STRING,
# MAGIC     refresh_frequency STRING,
# MAGIC     owner STRING,
# MAGIC     description STRING
# MAGIC );
# MAGIC 


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'bronze_batch_log',
# MAGIC  'bronze',
# MAGIC  'batchid',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Log of data ingestion o bronze'
# MAGIC );
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'tbl_rawEmotiondata',
# MAGIC  'bronze',
# MAGIC  'event_date + employee_id + department',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Daily data dump of emotions'
# MAGIC );
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'silver_emotions_events',
# MAGIC  'silver',
# MAGIC  'event_date + employee_id + department',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Cleaned and validated Emotion data'
# MAGIC );
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'dimdate',
# MAGIC  'gold',
# MAGIC  'Date',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Date Dimention table'
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'dimdepartment',
# MAGIC  'gold',
# MAGIC  'id',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Department Dimention table'
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'emotion_trend_daily',
# MAGIC  'gold',
# MAGIC  'event_date+emotion_type+department_id',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Daily emotion trend metrics for analytics'
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'gold_burnout_daily_metrics',
# MAGIC  'gold',
# MAGIC  'event_date+department_id',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Daily Burnout metrics'
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'gold_sentiment_daily',
# MAGIC  'gold',
# MAGIC  'event_date+department_id+sentiment_bucket',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Daily sentiments'
# MAGIC );
# MAGIC 
# MAGIC INSERT INTO table_metadata VALUES
# MAGIC (
# MAGIC  'invalid_emotion_events',
# MAGIC  'quarrentine',
# MAGIC  'event_date+employee_id+error_message',
# MAGIC  'daily',
# MAGIC  'InsightFabric-Contributors',
# MAGIC  'Invalid reors from silver layer to audit'
# MAGIC );

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
