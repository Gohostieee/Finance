import mysql.connector
from dotenv import load_dotenv, find_dotenv
from mysql.connector.constants import ClientFlag
import json,os




load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect(user=dbKeys["user"],password=dbKeys["password"],host=dbKeys["host"],database=dbKeys["dbName"])

cursor = connection.cursor()

#cursor.execute("insert into apiKeys values('AscateraxAnya')")
#cursor.execute("create table apiKeys (apiKey varchar(255))")
#connection.commit()
#cursor.execute('alter table coinPriceData drop primary key,add column id int not null auto_increment, add primary key (Id)')
#cursor.execute('desc coinPriceData')
#connection.commit()
#cursor.execute("select date from coinPriceData where date = ('2022-04-26')")
cursor.execute('select * from coinPriceData')
if cursor.fetchone() == None:
	print('faux')

for x in cursor.fetchall():
	print(x)
