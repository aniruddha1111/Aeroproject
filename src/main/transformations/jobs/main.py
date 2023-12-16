import logging
import os

from resources.dev import config
from src.main.utility.encrypt_decrypt import decrypt
from src.main.utility.s3_client_object import *
from src.main.utility.my_sql_session import *
from src.main.utility.logging_config import *

aws_access_key=config.aws_access_key
aws_secret_key=config.aws_secret_key

s3_client_provider = S3ClientProvider(aws_access_key,aws_secret_key)
s3_client = s3_client_provider.get_client()

response= s3_client.list_buckets()
print(response['Buckets'])
logger.info("List of buckets:%s",response['Buckets'])


csv_files=[file for file in os.listdir(config.local_directory) if file.endswith(".csv")]
connection=get_mysql_connection();
cursor=connection.cursor()

total_csv_files=[]
if csv_files:
    for file in csv_files:
        total_csv_files.append(file)
    statement=f"Select file_name from product_staging_table where file_name in ({str(total_csv_files)[1:-1]}) and status='I'"
    logger.info(f"dynamically statement created {statement}")
    cursor.execute(statement)
    data=cursor.fetchall()
    if data:
        logger.info("last run was successfull")
else:
    logger.info("Last run was unsuccesfull")


