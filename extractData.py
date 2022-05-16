from bs4 import BeautifulSoup
import urllib.request
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import itertools
import mysql.connector
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv, find_dotenv
#start the database//change according to your own credentials
def database_connect(hst,usr,passwrd,dtbs):
    global db
    global mycursor

    db = mysql.connector.connect(
        host=hst,
        user=usr,
        passwd=passwrd,
        database=dtbs


    )
    mycursor = db.cursor(buffered=True)




load_dotenv("./src/secret.env")
dbKeys = json.loads(os.getenv("googleCloud"))

print(dbKeys)
connection = mysql.connector.connect()


def split(word):
    return [char for char in word]
mycursor = None
#create the tables if non existant//should create a way to check if they exist//however at the time I was not taking the translation of this code into another database in mind
opts = Options()
opts.add_argument(' --headless'     )

opts.add_argument('--no-sandbox')
#enter the desired url//due to the nature of coinmarketcap and the way it was created dynamically this scraper might not work with other services
item = str('https://coinmarketcap.com/homepage-v21/')
#initialize the virtual browser
print("huh")
driver  = webdriver.Chrome("/usr/bin/chromedriver", options = opts)
print("huh")

driver.get(item)
print("huh")

#zoom out in order to load all of the content
driver.execute_script("document.body.style.zoom='5%'")
time.sleep(2)
#main scraper
def main_scraper(driver):
    print("wha")
    timeYMD = datetime.today().strftime('%Y-%m-%d')
    timeHMS = datetime.today().strftime('%H:%M:%S')
    print("wha")

    
    #get the html off the website
    print("wha")

    page = driver.execute_script('return document.body.innerHTML')
    print("wha")

    #list of words not desired when I scrape the information out
    nonoWords=('#','Name','Price','24h %','7d %','Market Cap','Volume(24h)','Circulating Supply', 'Last 7 Days','nigger')

    rowdy=[]
    counter=0
    print("wha")

    soup = BeautifulSoup(''.join(driver.page_source), 'html.parser')
    shenanigans=dict()
    itemss=0
    print("wha")

    #iterate through every single "tr" element inside the html//this is where these are all coins are stored
    for x in soup.find_all('tr'):
        print("whaevs")

        #print(len(x))
        #print(x[0])

        #print(type(x))
        #print(x.text)
        lists=list()
        for y in x:
            lists.append(y.text)
        #print(lists)
        for y in lists:
            #make sure the line that is being iterated through doesnt contain any of the illegal characters which we dont want
            if y.strip() not in nonoWords:
                #print(y)
                try:

                    int(y)+int(y)
                    rowdy=[]

                    counter=0
                except:
                    #a bunch of counter checks in order to see where in the data we currently are and taking steps in order to format it appropiately
                    if counter==0:
                        print(y)
                        for q in y:
                            if q.isdigit():
                                digit=str(q)
                                print(q,"for the macy")
                                rowdy.append(y.split(digit)[0])

                                break

                            print(y.split(q)[0],'go home')

                        counter+=1
                    elif counter in range(1,4):
                        #take every single string and what ever the number is replace any rouge characters with nothing so that we can convert it into a int type variable instead of a string

                        rowdy.append(y.replace('%','').replace('%','').replace('$','').replace(',',''))
                        counter+=1
                    elif counter==4:
                    #    print('what? \n',y)
                    #    print('gmc',y.split('$')[2])
                        rowdy.append(y.split('$')[2].replace(',',''))
                        counter+=1
                        theSplit=0
                    elif counter in range(5,8):
                        print(y,'radish')

                        for k in y.split(','):
                            print(k,'carrots')

                            if len(k.replace('$',''))>3 and theSplit==0:
                            #    print(k.split()[isdigit()],k.split(),'apples')
                                theSplit=''.join(split(k)[:3])
                                print(theSplit,'cucumbers')
                                #                            theSplit=''.join(split(k)[:3])

                                #    print(y.split(theSplit)[0],theSplit,'cucumbers',y.split(theSplit)[1])
                                rowdy.append(y.split(theSplit)[0].replace('$','').replace(',','').strip()+theSplit)
                                rowdy.append(y.split(theSplit)[1].split(' ')[0].replace('$','').replace(',','').strip())
                                #after all of this the data will be properly formated and printed out in a neatly matter ready to be inserted into our database
                                print(rowdy)
                        print(rowdy,'cavendish')
                          #print('cavish',len(rowdy))
                        counter+=1
                        if counter==7:
                            try:
                                print(rowdy[0],'Corn')
                                #insert the data into a table inside of sql by using the integrated %s method instead of the insecure string formatting
                                mycursor.execute('INSERT INTO coinPriceData(name,price,dailyRate,weeklyRate,marketCap,dailyVolume,circulatingSupply,date,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (rowdy[0],rowdy[1],rowdy[2],rowdy[3],rowdy[4],rowdy[5],rowdy[6],timeYMD,timeHMS))
                                #commit the changes
                                db.commit()
                            except:
                                #in some conditions the previous statement will throw an error and instead of saying insert we should say update/set
                                print(rowdy[0],'Corn')
                                mycursor.execute('UPDATE coinPriceData SET price=%s,dailyRate=%s,weeklyRate=%s,marketCap=%s,dailyVolume=%s,circulatingSupply=%s,date=%s,time=%s WHERE name=%s ', (rowdy[1],rowdy[2],rowdy[3],rowdy[4],rowdy[5],rowdy[6],timeYMD,timeHMS,rowdy[0]))
                                #mycursor.execute('INSERT INTO Coinbbbb(name,price,dailyRate,weeklyRate,marketCap,dailyVolume,circulatingSupply,date,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (rowdy[0],rowdy[1],rowdy[2],rowdy[3],rowdy[4],rowdy[5],rowdy[6],datetime.today().strftime('%Y-%m-%d'),datetime.today().strftime('%H:%M:%S')))
                                db.commit()






if __name__=="__main__":
    while True:
        database_connect(usr=dbKeys["user"],passwrd=dbKeys["password"],hst=dbKeys["host"],dtbs=dbKeys["dbName"])
        main_scraper(driver)
        time.sleep(60)
