from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType


NUMERICAL_FEATURES = [f"integer_feature_{index}" for index in range(1, 14)]
CATEGORICAL_FEATURES = [f"categorical_feature_{index}" for index in range(1, 27)]
FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


def build_feature_schema() -> StructType:
    fields = [
        StructField("integer_feature_1", DoubleType(), True),
        StructField("integer_feature_2", DoubleType(), True),
        StructField("integer_feature_3", DoubleType(), True),
        StructField("integer_feature_4", DoubleType(), True),
        StructField("integer_feature_5", DoubleType(), True),
        StructField("integer_feature_6", DoubleType(), True),
        StructField("integer_feature_7", DoubleType(), True),
        StructField("integer_feature_8", IntegerType(), True),
        StructField("integer_feature_9", IntegerType(), True),
        StructField("integer_feature_10", DoubleType(), True),
        StructField("integer_feature_11", DoubleType(), True),
        StructField("integer_feature_12", DoubleType(), True),
        StructField("integer_feature_13", DoubleType(), True),
    ]

    fields.extend(
        StructField(feature_name, StringType(), True)
        for feature_name in CATEGORICAL_FEATURES
    )

    return StructType(fields)


def build_event_schema() -> StructType:
    return StructType(
        [
            StructField("event_id", StringType(), False),
            StructField("timestamp", StringType(), False),
            StructField("features", build_feature_schema(), False),
        ]
    )
