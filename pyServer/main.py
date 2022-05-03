from flask import Flask
from flask import request
import mysql.connector
from dotenv import load_dotenv, find_dotenv
import os,json
from apiFunc import _dateRange,listIntoSqlQuery,dateFormatter,stringIntoList
from mysql.connector.constants import ClientFlag



load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect(user=dbKeys["user"],password=dbKeys["password"],host=dbKeys["host"],database=dbKeys["dbName"])

cursor = connection.cursor()
#cursor.execute("select date from coinPriceData where date in ('2022-05-01') ")
#print(cursor.fetchall())
#input()
app = Flask(__name__)
@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/api', methods=['GET', 'POST'])
def apiRequest():

    apikey = request.args.get('apiKey')
    print(apikey)
    cursor.execute("select * from apiKeys where apiKey = (%s)",(apikey,))

    keyCheck = cursor.fetchall()
    if keyCheck:
        print("checked")
        query = request.args.get('query')
        match query:
            case "interdaily":
                start = request.args.get('start')
                end = request.args.get('end')
                nameRange = tuple(stringIntoList(request.args.get('names'),","))
                dateRange = tuple([x for x in _dateRange(start,end)])
                queryStringDates = ','.join(['%s'] * len(dateRange))
                queryStringNames = ','.join(['%s'] * len(nameRange))
                totalRange =  dateRange + nameRange 
                queryString= f"select * from coinPriceData where   date in ({queryStringDates}) and name in ({queryStringNames}) "
               # print("select * from coinPriceData where   date in (%s) and name in  ",dateRange)
                print(cursor.execute(queryString,totalRange))
                print(cursor.statement)
                return {'response':cursor.fetchall()}
            case default:
                return {'response':'RON you moronic new nigga'}
    else:
        print("failed")
    return {"response":keyCheck}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)