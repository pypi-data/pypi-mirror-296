from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
)

BRONZE_METADATA_SCHEMA = StructType(
    [
        StructField("bronze_data_table", StringType(), False),
        StructField("source_system", StringType(), False),
        StructField("source_type", StringType(), False),
        StructField("source_name", StringType(), False),
        StructField("updated_at", StringType(), False),
    ]
)

BRONZE_INGESTION_LOG_SCHEMA = StructType(
    [
        StructField("ingested_timestamp", StringType(), False),
        StructField("source_name", StringType(), False),
        StructField("source_count", IntegerType(), False),
        StructField("bronze_data_table", StringType(), False),
        StructField("bronze_data_count", IntegerType(), False),
        StructField("status", StringType(), False),
    ]
)
