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

# get data
#spark.sql("USE LhInsightFabric")
df_silver = spark.table("LhInsightFabric.silver.silver_emotion_events")
df_silver.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


from pyspark.sql.functions import sequence, explode, lit, col, min, max, year, month, dayofmonth, dayofweek, date_format

# creating a date table for using as primary key 

date_range = df_silver.select(
    min(col("event_date")).alias("min_date"),
    max(col("event_date")).alias("max_date")
).collect()[0]

min_date = date_range["min_date"]
max_date = date_range["max_date"]

date_df = spark.createDataFrame([(min_date, max_date)], ["start", "end"]) \
    .withColumn("Date", explode(sequence(col("start"), col("end")))) \
    .select("Date")

dimDate_df = date_df.withColumn("Year", year(col("Date"))) \
    .withColumn("Month", month(col("Date"))) \
    .withColumn("Day", dayofmonth(col("Date"))) \
    .withColumn("DayOfWeek", dayofweek(col("Date"))) \
    .withColumn("MonthName", date_format(col("Date"), "MMM")) \
    .withColumn("YearMonth", date_format(col("Date"), "yyyyMM")) \
    .withColumn("DateKey", date_format(col("Date"), "yyyyMMdd").cast("int"))

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.gold.DimDate")
dimDate_df.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("LhInsightFabric.gold.DimDate")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


df_DimDepartment=(df_silver.select(col("department"))).distinct()
df_DimDepartment.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

# Define a window over the entire dataframe
window_spec = Window.orderBy("department")  

df_DimDepartment = df_DimDepartment.withColumn("id", row_number().over(window_spec))
df_DimDepartment.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.gold.DimDepartment")
df_DimDepartment.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("LhInsightFabric.gold.DimDepartment")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_silver = df_silver.withColumnRenamed("department", "department_text")

silver = df_silver.alias("silver")
dim = df_DimDepartment.alias("dim")

df_silver_deptid = (
    silver.join(
        dim,
        silver["department_text"] == dim["department"],
        "left"
    )
    .withColumn("department_id", dim["id"])   # create new FK column
    .drop("department_text")                  # drop from silver
    .drop(dim["department"])                  # drop from dim
    .drop(dim["id"])                          # drop dim.id after copying
)

df_silver_deptid.show()




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import (
    col, count, avg, sum, round
)

# Daily aggregation per emotion
df_gold_daily = (
    df_silver_deptid
    .groupBy("event_date", "emotion_type","department_id")
    .agg(
        count("*").alias("emotion_count"),
        round(avg("intensity"), 3).alias("avg_emotion_score")
    )
)
df_gold_daily.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_daily_total = (
    df_gold_daily
    .groupBy("event_date","department_id")
    .agg(
        sum("emotion_count").alias("total_count")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import round

df_gold_trend = (
    df_gold_daily
    .join(df_daily_total, ["event_date","department_id"], how="left")
    .withColumn(
        "emotion_percentage",
        round((col("emotion_count") / col("total_count")) * 100, 2)
    )
    .drop("total_count")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import concat_ws

df_gold_trend = df_gold_trend.withColumn(
    "event_dept_key",
    concat_ws("-", col("event_date"), col("department_id"))
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.gold.emotion_trend_daily")


df_gold_trend.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("LhInsightFabric.gold.emotion_trend_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Burnout trend**

# CELL ********************

#Daily Negative Emotion Score

from pyspark.sql.functions import avg, count, round, when

df_daily = (
    df_silver_deptid
    .groupBy("event_date", "department_id")
    .agg(
        count("*").alias("total_events"),
        sum(when(col("sentiment_bucket") == "Negative", 1).otherwise(0)).alias("negative_events"),
        round(avg(
            when(col("sentiment_bucket") == "Negative", col("intensity"))
        ), 3).alias("avg_negative_intensity")
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_daily = df_daily.withColumn(
    "negative_ratio",
    round(col("negative_events") / col("total_events"), 3)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#7-Day Rolling Average (Core Burnout Logic)

from pyspark.sql.window import Window
from pyspark.sql.functions import avg as _avg, unix_timestamp

df_daily = df_daily.withColumn(
    "event_day_ts",
    unix_timestamp(col("event_date"))
)
window_7d = (
    Window
    .partitionBy("department_id")
    .orderBy(col("event_day_ts"))
    .rangeBetween(-6 * 86400, 0)   # last 7 days incl today
)

df_burnout_rolling = (
    df_daily
    .withColumn(
        "rolling_7d_negative_avg",
        round(_avg("negative_ratio").over(window_7d), 3)
    )
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Burnout Risk Classification

from pyspark.sql.functions import when

df_burnout_final = (
    df_burnout_rolling
    .withColumn(
        "burnout_level",
        when(col("rolling_7d_negative_avg") >= 0.17, "High")
        .when(col("rolling_7d_negative_avg") >= 0.14, "Medium")
        .otherwise("Low")
    )
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_burnout_final.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import concat_ws

df_burnout_final = df_burnout_final.withColumn(
    "event_dept_key",
    concat_ws("-", col("event_date"), col("department_id"))
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.gold.gold_burnout_daily_metrics")

df_burnout_final.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("LhInsightFabric.gold.gold_burnout_daily_metrics")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# <u>**Positive vs Negative Sentiment**</u>
# _Is the overall emotional state improving or declining?
# _

# CELL ********************

# Daily Sentiment Counts
df_sentiment_daily = (
    df_silver_deptid
    .groupBy("event_date","department_id", "sentiment_bucket")
    .agg(
        count("*").alias("sentiment_count")
    )
)

#Calculate Daily Percentages

df_daily_total = (
    df_sentiment_daily
    .groupBy("event_date","department_id")
    .agg(
        sum("sentiment_count").alias("total_count")
    )
)

df_sentiment_gold = (
    df_sentiment_daily
    .join(df_daily_total, ["event_date", "department_id"], "left")
    .withColumn(
        "sentiment_percentage",
        round((col("sentiment_count") / col("total_count")) * 100, 2)
    )
    .drop("total_count")
)

#Net Sentiment Score

df_net_sentiment = (
    df_sentiment_gold
    .withColumn(
        "net_sentiment_score",
        when(col("sentiment_bucket") == "Positive", col("sentiment_percentage"))
        .when(col("sentiment_bucket") == "Negative", -col("sentiment_percentage"))
        .otherwise(0)
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import concat_ws

df_net_sentiment = df_net_sentiment.withColumn(
    "event_dept_key",
    concat_ws("-", col("event_date"), col("department_id"))
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("DROP TABLE IF EXISTS LhInsightFabric.gold.gold_sentiment_daily")
df_net_sentiment.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("LhInsightFabric.gold.gold_sentiment_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
