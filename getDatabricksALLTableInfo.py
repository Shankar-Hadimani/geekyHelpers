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
    if 'binocs' in db_name or 'f_bison' in db_name:
        
        db_dict[db_name] = []
        
        table_df = spark.sql("show tables in {db}".format(db=db_name))

        # iterate via tables and append to db_dict
        for tbl_row in table_df.rdd.collect():
            tbl_name = tbl_row["tableName"]

            prop_df = spark.sql("DESCRIBE EXTENDED {db}.{tbl}".format(db=db_name, tbl=tbl_name))
            for prop_row in prop_df.rdd.collect():
                if prop_row["col_name"] == "Location":
                    location = prop_row["data_type"]
                    db_dict[db_name].append((tbl_name, location))

Table = Row("databaseName", "tableName", "location")
table_seq = []
for db, tables in db_dict.items():
    for table_props in tables:
        table_name = table_props[0]
        table_location = table_props[1]
        table_seq.append(Table(db, table_name, table_location))

df1 = spark.createDataFrame(table_seq)

# COMMAND ----------
# df1 = spark.createDataFrame(table_seq)

df1 = df1.select('databaseName', 'tableName','location')
df1 = df1.withColumn( "sysname" ,reverse(split('databaseName','_'))[0]) 
display(df1)
