# Ref: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe

import json
import os
from datetime import datetime

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


keyfile = os.environ.get("KEYFILE_PATH")
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "dataengineerbootcamp-385813"
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)
# order_id,created_at,order_cost,shipping_cost,order_total,order_total,shipping_service,estimated_delivery_at,delivered_at,status,user,promo,address
job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    schema=[
        bigquery.SchemaField("order_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("created_at", bigquery.SqlTypeNames.TIMESTAMP),
        bigquery.SchemaField("order_cost", bigquery.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("shipping_cost", bigquery.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("order_total", bigquery.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("shipping_service", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("estimated_delivery_at", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("delivered_at", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("status", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("user", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("promo", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("address", bigquery.SqlTypeNames.STRING),
    ],
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    ),
    # clustering_fields=["first_name", "last_name"],
)

file_path = "./data/orders.csv"
df = pd.read_csv(file_path, parse_dates=["created_at"])
df.info()

table_id = f"{project_id}.deb_bootcamp.orders"
job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result()

table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")