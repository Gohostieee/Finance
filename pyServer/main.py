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

app = Flask(__name__)

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
                return extractDatePrice(request,cursor)
            case default:
                return {'response':'500 server error'}
    else:
        print("failed")

        return {"response":"key " + keyCheck + " failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
