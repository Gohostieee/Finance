import mysql.connector
from dotenv import load_dotenv, find_dotenv
from mysql.connector.constants import ClientFlag
import json,os




load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect(user=dbKeys["user"],password=dbKeys["password"],host=dbKeys["host"],database=dbKeys["dbName"])

cursor = connection.cursor()

cursor.execute('CREATE TABLE coinPriceData (name VARCHAR(50) PRIMARY KEY, price float, dailyRate float, weeklyRate float,marketCap BIGINT,dailyVolume float, circulatingSupply float, date VARCHAR(50), time VARCHAR(50))')
connection.commit()