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
# MAGIC CREATE TABLE IF NOT EXISTS Bronze.bronze_batch_log (
# MAGIC     batch_id STRING,
# MAGIC     data_ingested_on TIMESTAMP,
# MAGIC     record_count INT,
# MAGIC     silver_processed BOOLEAN
# MAGIC )
# MAGIC 


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

max_batch_df = spark.sql("SELECT max(Batch_RunId) as max_id FROM bronze.tbl_rawEmotiondata")
current_batch_id = max_batch_df.collect()[0]['max_id']

count_df = spark.sql(f"SELECT count(*) as total FROM bronze.tbl_rawEmotiondata WHERE Batch_RunId = '{current_batch_id}'")
record_count = count_df.collect()[0]['total']
query = f"""
INSERT INTO bronze.bronze_batch_log (batch_id, data_ingested_on, record_count, silver_processed)
VALUES ('{current_batch_id}', current_timestamp(), {record_count}, false)
"""
spark.sql(query)

print(f"Logged Batch {current_batch_id} with {record_count} records.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
