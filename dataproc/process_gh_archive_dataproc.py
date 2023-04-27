
import argparse

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Date in format YYYY-MM-DD", required=True)
    parser.add_argument("--source_files_pattern", help="Source files pattern for the GH archive to process.", required=True)
    parser.add_argument("--destination_files_pattern", help="Destination files pattern for the GH archive to process.", required=True)

    args = parser.parse_args()
    date = args.date

    read_filepath = args.source_files_pattern
    write_filepath = args.destination_files_pattern
    read_filepath=read_filepath.format(date)
    print(f"date received: {date}")

    spark = SparkSession.builder.master("yarn").appName('GCSFilesRead').getOrCreate()

    print(f"read_filepath: {read_filepath}")
    df = spark.read.json(read_filepath)

    allowed_events = [
        "PushEvent",
        "ForkEvent",
        "PublicEvent",
        "WatchEvent",
        "PullRequestEvent",
    ]

    main_df = df.select(
        F.col("id").alias("event_id"),
        F.col("type").alias("event_type"),
        F.to_timestamp( F.col("created_at"), "yyyy-MM-dd'T'HH:mm:ss'Z'" ).alias("created_at"),
        F.col("repo.id").alias("repository_id"),
        F.col("repo.name").alias("repository_name"),
        F.col("repo.url").alias("repository_url"),
        F.col("actor.id").alias("user_id"),
        F.col("actor.login").alias("user_name"),
        F.col("actor.url").alias("user_url"),
        F.col("actor.avatar_url").alias("user_avatar_url"),
        F.col("org.id").alias("org_id"),
        F.col("org.login").alias("org_name"),
        F.col("org.url").alias("org_url"),
        F.col("org.avatar_url").alias("org_avatar_url"),
        F.col("payload.push_id").alias("push_id"),
        F.col("payload.distinct_size").alias("number_of_commits"),
        F.col("payload.pull_request.base.repo.language").alias("language"),
    ).filter(
        F.col("type").isin(allowed_events)
    )

    main_df = main_df.withColumn("year", F.year("created_at")) \
        .withColumn("month", F.month("created_at")) \
        .withColumn("day", F.dayofmonth("created_at")) \
        .withColumn("hour", F.hour("created_at")) \
        .withColumn("minute", F.minute("created_at")) \
        .withColumn("second", F.second("created_at"))


    # write the DataFrame to GCS partitioned by year, month, and day and bucketed by hour and minute
    date = date.replace("-", "")

    main_df.write \
    .partitionBy("year", "month", "day") \
    .bucketBy(24, "hour") \
    .sortBy("hour", "minute") \
    .option("path", write_filepath) \
    .option("header", True) \
    .mode("append") \
    .saveAsTable(f"table{date}")
