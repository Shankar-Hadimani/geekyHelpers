# Databricks notebook source
from pyspark.sql import *
from pyspark.sql.functions import *
import re


db_dict = {}

# load database names
df = spark.sql("show databases")

# iterate thru each database
for db_row in df.rdd.collect():
  
    db_name = db_row["databaseName"]
  
    # only capture database begins with "f_erp"
    if 'u_quality_' in db_name or 'u_' in db_name:
        
        db_dict[db_name] = []
        
        table_df = spark.sql("show tables in {db}".format(db=db_name))

        # iterate via tables and append to db_dict
        for tbl_row in table_df.rdd.collect():
            tbl_name = tbl_row["tableName"]
            #print(db_name, tbl_name)
            prop_df = spark.sql("""SHOW CREATE TABLE  {db}.{tbl}""".format(db=db_name, tbl=tbl_name))
            for prop_row in prop_df.rdd.collect()[:1]:
              if prop_row["createtab_stmt"]:
                header_marker = "--=========================================================="
                header_comment = """--                  {tbl}""".format(db=db_name, tbl=tbl_name)
                prefix_text = """IF NOT EXISTS ( SELECT * FROM sys.external_tables WHERE object_id = OBJECT_ID('{db}.{tbl}') )""".format(db=db_name, tbl=tbl_name)
                trailer_text = ",\n DATA_SOURCE = [<SchemaName>] , \n FILE_FORMAT = [_delta_format] ) \nGO "
                createtab_stmt = (prop_row["createtab_stmt"]
                                  .replace('CREATE TABLE','CREATE EXTERNAL TABLE ')
                                  .replace('STRING','NVARCHAR(max)')
                                  .replace('TIMESTAMP','DATETIME2')
                                  .replace('USING delta', 'WITH (')
                                  .replace('abfss://<ADLSDatalakeContainerName>@<ADLSDatalakeName>.dfs.core.windows.net/','')
                                  .replace("LOCATION", "LOCATION = ")
                                 )
                createtab_stmt = '\n'+header_marker +'\n'+header_comment + '\n'+ header_marker +'\n' +prefix_text + '\n' + createtab_stmt + trailer_text
                p = re.compile(r"\`(.*?)\`")
                result = re.sub(p, r"[\1]", createtab_stmt)
                db_dict[db_name].append((tbl_name, result))

Table = Row("databaseName", "tableName", "createtab_stmt")
table_seq = []
for db, tables in db_dict.items():
    for table_props in tables:
        table_name = table_props[0]
        table_location = table_props[1]
        table_seq.append(Table(db, table_name, table_location))

df1 = spark.createDataFrame(table_seq)
df1 = df1.select('databaseName', 'tableName','createtab_stmt')
display(df1)