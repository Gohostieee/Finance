import mysql.connector
from dotenv import load_dotenv, find_dotenv
from mysql.connector.constants import ClientFlag
import json,os




load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect(user=dbKeys["user"],password=dbKeys["password"],host=dbKeys["host"],database=dbKeys["dbName"])

cursor = connection.cursor()
#cursor.execute('alter table coinPriceData drop primary key,add column id int not null auto_increment, add primary key (Id)')
#cursor.execute('desc coinPriceData')

cursor.execute('select * from coinPriceData')
for x in cursor.fetchall():
	print(x)
