# Databricks notebook source
from pyspark.sql import *
from pyspark.sql.functions import *

db_dict = {}

# load database names
df = spark.sql("show databases")

# iterate thru each database
for db_row in df.rdd.collect():
  
    db_name = db_row["databaseName"]
  
    # only capture database begins with "f_erp"
    if 'u_XXXXXXXXXX' in db_name or 'f_XXXXXXXXXX' in db_name:
        
        db_dict[db_name] = []
        
        table_df = spark.sql("show tables in {db}".format(db=db_name))

        # iterate via tables and append to db_dict
        for tbl_row in table_df.rdd.collect():
            tbl_name = tbl_row["tableName"]

            prop_df = spark.sql("SELECT '{tbl}' AS table_name, count(1) AS row_cnt FROM {db}.{tbl}".format(db=db_name, tbl=tbl_name))
            for prop_row in prop_df.rdd.collect():
              db_dict[db_name].append((tbl_name,prop_row['table_name'],prop_row['row_cnt']))

Table = Row("databaseName", "tableName", "tableName1","row_cnt")
table_seq = []
for db, tables in db_dict.items():
    for table_props in tables:
        table_name = table_props[0]
        tableName1 = table_props[1]
        row_cnt = table_props[2]
        table_seq.append(Table(db, table_name, tableName1, row_cnt))

df1 = spark.createDataFrame(table_seq)
display(df1)
