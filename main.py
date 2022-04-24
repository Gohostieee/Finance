import os
import json
import finnhub
import requests

import mysql.connector
from dotenv import load_dotenv, find_dotenv
from mysql.connector.constants import ClientFlag





load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect(user=dbKeys["user"],password=dbKeys["password"],host=dbKeys["host"],database=dbKeys["dbName"])

cursor = connection.cursor()
url = "https://alpha-vantage.p.rapidapi.com/query"

querystring = {"market":"USD","symbol":"ETH","function":"DIGITAL_CURRENCY_DAILY"}

headers = {
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com",
	"X-RapidAPI-Key": "d124bbf6cemsh164e7f21e5e7988p16c2c7jsn424260bb6bcb"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(json.loads(response.text)["Meta Data"])

"""
# Setup client
finnhub_client = finnhub.Client(api_key=os.getenv("finhubKey"))
res = finnhub_client.general_news('general', min_id=0)

#Convert to Pandas Dataframe
import pandas as pd
pdTable = pd.DataFrame(res)

print(pdTable["datetime"])

#italians

db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=dbKeys["user"],  # e.g. "my-database-user"
        password=dbKeys["password"],  # e.g. "my-database-password"
        database=dbKeys["dbName"],  # e.g. "my-database-name"
        query={
            "unix_socket": "{}/{}".format(
                db_socket_dir,  # e.g. "/cloudsql"
                dbKeys["instanceConnection"])  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
        }
    ),
    **db_config
)
"""