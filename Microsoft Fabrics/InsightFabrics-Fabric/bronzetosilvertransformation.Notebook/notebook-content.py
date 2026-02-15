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

# MAGIC %%configure -f
# MAGIC {
# MAGIC     "defaultLakehouse": {
# MAGIC         "name": "LhInsightFabric",
# MAGIC         "id": "baf1fc42-d907-4f03-a097-08b602d8a0c8",
# MAGIC         "workspaceId": "bc7938fc-605d-41ac-ac76-fb76a0c0cac4"
# MAGIC     }
# MAGIC }

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
bronze_df = spark.table("LhInsightFabric.bronze.tbl_rawEmotiondata")
bronze_df.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Remove rows where critical columns are null
clean_df = bronze_df.dropna(subset=["emotion", "score", "text","employee_id"])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#trim and clean strings

from pyspark.sql.functions import trim
from pyspark.sql.functions import col
clean_df= clean_df.withColumn("emotion",trim(col("emotion"))) \
                .withColumn("employee_name",trim(col("employee_name"))) \
                .withColumn("department",trim(col("department"))) \
                .withColumn("score",trim(col("score"))) \
                .withColumn("employee_id",trim(col("employee_id"))) 
clean_df.show(5)                

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, when,concat,coalesce,lit

# Initialize error_message column
clean_df = clean_df.withColumn("error_message", lit(""))

# Add error messages for intensity
error_df = clean_df.withColumn(
    "error_message",
    when(col("score").isNull(), "Intensity is null;")
    .when(~col("score").cast("int").isNotNull(), "Intensity is not an integer;")  # catches invalid types
    .when((col("score").cast("int") < 1) | (col("score").cast("int") > 10), "Intensity should be between 1 and 10;")
    .otherwise(col("error_message"))
)

# Add error messages for Emotion

error_df = clean_df.withColumn(
    "error_message",
    when(col("emotion").isNull(), concat(coalesce(col("error_message"), lit("")), lit("Emotion is null; ")))
    .when(col("emotion")=="",  concat(coalesce(col("error_message"), lit("")), lit("Emotion Empty")))
    .otherwise(col("error_message"))
)

# Add error messages for employee id
error_df = clean_df.withColumn(
    "error_message",
    when(col("employee_id").isNull(),  concat(coalesce(col("error_message"), lit("")), lit("employee_id is null; ")))
    .when(~col("employee_id").cast("int").isNotNull(),  concat(coalesce(col("error_message"), lit("")), lit("employee_id is not an integer;")))
      # catches invalid types
    .otherwise(col("error_message"))

)

# Add error messages for department

error_df = clean_df.withColumn(
    "error_message",
    when(col("department").isNull(), concat(coalesce(col("error_message"), lit("")), lit("department is null; ")))
    .when(col("department")=="",  concat(coalesce(col("error_message"), lit("")), lit("department Empty")))
    .otherwise(col("error_message"))
)

clean_df.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# clean_df.select( to_timestamp(regexp_replace(col("created_at").substr(1, 23),"T"," "))).show(truncate=False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

clean_df.printSchema()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

clean_df.limit(5).show(truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

clean_df.filter(col("created_at").isNull()).show(20,False)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import to_timestamp, regexp_replace,substring

silver_df = clean_df.withColumn(
    "event_timestamp",
    to_timestamp(
        substring(
            regexp_replace(col("created_at"), "T", " "),
            1,
            19
        ),
        "yyyy-MM-dd HH:mm:ss"
    )
)

silver_df.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_df.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add error messages for date

error_df = silver_df.withColumn(
    "error_message",
    when(col("event_timestamp").isNull(), concat(coalesce(col("error_message"), lit("")), lit("Time is not valid; ")))
    .otherwise(col("error_message"))
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

silver_df.filter(col("event_timestamp").isNull()).show(20, False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# seperate valid and invalid rows

from pyspark.sql.functions import to_date

df_valid = (
    silver_df
    .filter(col("error_message").isNull() | (col("error_message") == ""))
    .select(
        col("id"),
        col("index"),
        col("emotion").alias("emotion_type"),
        col("score").alias("intensity"),
        col("text").alias("reason"),
        col("employee_name"),
        col("employee_id"),
        col("department"),
        col("event_timestamp")
    )
)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# seperate valid and invalid rows

from pyspark.sql.functions import to_date

df_Invalid = (
    error_df
    .filter(col("error_message").isNull() | (col("error_message") == ""))
    .select(
        col("id"),
        col("index"),
        col("emotion").alias("emotion_type"),
        col("score").alias("intensity"),
        col("text").alias("reason"),
        col("employee_name"),
        col("employee_id"),
        col("department"),
        col("event_timestamp"),
        col("error_message")
    )
)

df_Invalid.write.mode("append").format("delta").saveAsTable("LhInsightFabric.quarrentine.Invalid_emotion_events")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


df_valid.filter(col("event_timestamp").isNull()).show(20, False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import to_date,year,month,date_format

df_valid = df_valid.withColumn(
    "event_date",
    to_date(  col("event_timestamp") , "yyyy-MM-dd"
    )
)


df_valid = df_valid.withColumn(
    "event_year",
    year(  col("event_timestamp")
    )
)


df_valid = df_valid.withColumn(
    "event_Month",
    month(  col("event_timestamp") 
    )
)


df_valid = df_valid.withColumn(
    "event_month_name",
    date_format(col("event_timestamp"), "MMMM")
)
df_valid = df_valid.withColumn(
    "event_weekday_name",
    date_format(col("event_timestamp"), "EEEE")
)

df_valid.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_valid.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


from pyspark.sql.functions import col, when, lower

df_valid = (
    df_valid
    .withColumn("emotion_type", lower(col("emotion_type")))
    .withColumn(
        "sentiment_bucket",
        when(col("emotion_type").isin("happy", "excited", "calm"), "Positive")
        .when(col("emotion_type") == "neutral", "Neutral")
        .when(col("emotion_type").isin("stress", "angry", "sad", "fear"), "Negative")
        .otherwise("Neutral")
    )
  
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

professional_keywords = [
    "work", "office", "deadline", "manager", "team", "deployed",
    "task", "feature", "production", "deployment", "build", "code"
]

personal_keywords = [
    "family", "child", "baby", "health", "sleep", "home",
    "relationship", "sick", "stress", "money", "personal"
]
df_valid = df_valid.withColumn("reason_lower", lower(col("reason")))

df_valid = df_valid.withColumn(
    "reason_type",
    when(col("reason_lower").rlike("|".join(professional_keywords)), "Professional")
    .when(col("reason_lower").rlike("|".join(personal_keywords)), "Personal")
    .otherwise("Unknown")
)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.silver.silver_emotion_events")

df_valid.write.mode("append").format("delta").saveAsTable("LhInsightFabric.silver.silver_emotion_events")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
