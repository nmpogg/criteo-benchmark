CREATE DATABASE IF NOT EXISTS ctr_lake;
USE ctr_lake;

CREATE EXTERNAL TABLE IF NOT EXISTS raw_events (
    event_id STRING,
    event_timestamp STRING,
    event_time TIMESTAMP,
    processing_time TIMESTAMP,
    kafka_topic STRING,
    kafka_partition INT,
    kafka_offset BIGINT,
    kafka_timestamp TIMESTAMP,
    raw_json STRING
)
PARTITIONED BY (event_date DATE)
STORED AS PARQUET
LOCATION 'hdfs://hdfs-namenode:9000/user/ctr/lake/raw_events';

CREATE EXTERNAL TABLE IF NOT EXISTS processed_features (
    event_id STRING,
    event_timestamp STRING,
    event_time TIMESTAMP,
    processing_time TIMESTAMP,
    topic STRING,
    `partition` INT,
    `offset` BIGINT,
    kafka_timestamp TIMESTAMP,
    raw_json STRING,
    integer_feature_1 DOUBLE,
    integer_feature_2 DOUBLE,
    integer_feature_3 DOUBLE,
    integer_feature_4 DOUBLE,
    integer_feature_5 DOUBLE,
    integer_feature_6 DOUBLE,
    integer_feature_7 DOUBLE,
    integer_feature_8 INT,
    integer_feature_9 INT,
    integer_feature_10 DOUBLE,
    integer_feature_11 DOUBLE,
    integer_feature_12 DOUBLE,
    integer_feature_13 DOUBLE,
    categorical_feature_1 STRING,
    categorical_feature_2 STRING,
    categorical_feature_3 STRING,
    categorical_feature_4 STRING,
    categorical_feature_5 STRING,
    categorical_feature_6 STRING,
    categorical_feature_7 STRING,
    categorical_feature_8 STRING,
    categorical_feature_9 STRING,
    categorical_feature_10 STRING,
    categorical_feature_11 STRING,
    categorical_feature_12 STRING,
    categorical_feature_13 STRING,
    categorical_feature_14 STRING,
    categorical_feature_15 STRING,
    categorical_feature_16 STRING,
    categorical_feature_17 STRING,
    categorical_feature_18 STRING,
    categorical_feature_19 STRING,
    categorical_feature_20 STRING,
    categorical_feature_21 STRING,
    categorical_feature_22 STRING,
    categorical_feature_23 STRING,
    categorical_feature_24 STRING,
    categorical_feature_25 STRING,
    categorical_feature_26 STRING
)
PARTITIONED BY (event_date DATE)
STORED AS PARQUET
LOCATION 'hdfs://hdfs-namenode:9000/user/ctr/lake/processed_features';

CREATE EXTERNAL TABLE IF NOT EXISTS predictions (
    event_id STRING,
    event_timestamp TIMESTAMP,
    processing_time TIMESTAMP,
    kafka_topic STRING,
    kafka_partition INT,
    kafka_offset BIGINT,
    ctr_score DOUBLE,
    prediction_label INT,
    model_version STRING,
    raw_event STRING,
    features STRING
)
PARTITIONED BY (event_date DATE)
STORED AS PARQUET
LOCATION 'hdfs://hdfs-namenode:9000/user/ctr/lake/predictions';

MSCK REPAIR TABLE raw_events;
MSCK REPAIR TABLE processed_features;
MSCK REPAIR TABLE predictions;
