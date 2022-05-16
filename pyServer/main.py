from flask import Flask
from flask import request
import mysql.connector
from dotenv import load_dotenv, find_dotenv
import os,json
from apiFunc import _dateRange,listIntoSqlQuery,dateFormatter,stringIntoList,getNameDateQuery,getNameDatePriceQuery,extractDatePrice
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

    apikey = request.args.get('apikey')
    print(apikey)
    cursor.execute("select * from apiKeys where apiKey = (%s)",(apikey,))

    keyCheck = cursor.fetchall()
    if keyCheck:
        print("checked")
        query = request.args.get('query')
        match query:
            case "interdaily":
                queryString = getNameDateQuery(request)
                print(cursor.execute(queryString[2],queryString[1]+queryString[0]))
                return {'response':cursor.fetchall()}
            case "lowtohigh":
                """queryString = getNameDatePriceQuery(request)
                print(cursor.execute(queryString[2],queryString[1]+queryString[0]))
                priceHighLow = [[x for x in cursor.fetchall()],[]]
                currDate = [[priceHighLow[0][0][2],priceHighLow[0][0][2]],'',0,0]
                currDate[1]=priceHighLow[0][0][1]
                for x in priceHighLow[0]:
                    if x[1] != currDate[1]:
                        priceHighLow[1].append([x[0],currDate[1],[currDate[0][0], currDate[0][1]]])
                        print(currDate, "what")
                        currDate[0][0]=x[2]
                        currDate[0][1]=x[2]
                        currDate[1]=x[1]
                    if x[2]<currDate[0][0]:
                        print(currDate,x)

                        currDate[0][0]=x[2]
                    elif x[2]>currDate[0][1]:
                        currDate[0][1]=x[2]
"""
                return extractDatePrice(request,cursor)
            case default:
                return {'response':'RON you moronic new nigga'}
    else:
        print("failed")

        return {"response":"key " + keyCheck + " failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)