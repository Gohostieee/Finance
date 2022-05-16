from datetime import date, timedelta

def listIntoSqlQuery(lists):
	response = ""
	for x in lists:
		print(x)
		response = f"{response}{x},"

	return response
def dateFormatter(date):
	print(date,"carrot")
	try:
		year,month,day=date.split('-')
		if int(month)<10:month=f"0{month}"
		if int(day)<10:day=f"0{day}"
		"""for x in range(len(date.split('-'))):
			if len(date.split('-')[x]) < 3 and int(date.split('-')[x]) < 10 :
				print(date.split('-')[:x])
				try:
					date = f"{date.split('-')[:x]}-0{date.split('-')[x]}-{date.split('-')[x + 1:]}"
				except:
					pass"""
		print("wot",f"{year}-{month}-{day}")
		return f"{year}-{month}-{day}"
	except:
		pass	
def stringIntoList(stringVar, splitee):
	return [x for x in stringVar.split(splitee)]
#print(dateFormatter("2022-9-1"))
print(listIntoSqlQuery(['1','2','3']))

def _dateRange(start,end,rate='daily'):
	start = [int(x) for x in start.split("-")]
	end = [int(x) for x in end.split("-")]	
	print(start[0],start[1],start[2])
	start = date(start[2],start[1],start[0],) 
	end = date(end[2],end[1],end[0])    # perhaps date.now()

	delta = end - start   # returns timedelta
	match rate:
		case 'daily':
			return [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
		case 'weekly':
			return [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 7)]
def getNameDateQuery(request):
    start = request.args.get('start')
    end = request.args.get('end')
    rate = request.args.get('rate')
    match rate:
    	
        case 'weekly':
        	dateRange = tuple([x for x in _dateRange(start,end,'weekly')])
        case default:
            dateRange = tuple([x for x in _dateRange(start,end)])
    nameRange = tuple(stringIntoList(request.args.get('names'),","))
    queryStringDates = ','.join(['%s'] * len(dateRange))
    queryStringNames = ','.join(['%s'] * len(nameRange))
    queryString= f"select * from coinPriceData where   date in ({queryStringDates}) and name in ({queryStringNames}) "           
    print(queryString, "what")
    #totalRange =  dateRange + nameRange 
    return [nameRange,dateRange, queryString]

def getNameDatePriceQuery(request):
    start = request.args.get('start')
    end = request.args.get('end')
    rate = request.args.get('rate')

    nameRange = tuple(stringIntoList(request.args.get('names'),","))
    match rate:
    	
        case 'weekly':
        	dateRange = tuple([x for x in _dateRange(start,end,'weekly')])
        case default:
            dateRange = tuple([x for x in _dateRange(start,end)])

    queryStringDates = ','.join(['%s'] * len(dateRange))
    queryStringNames = ','.join(['%s'] * len(nameRange))
    queryString= f"select name,date,price from coinPriceData where   date in ({queryStringDates}) and name in ({queryStringNames}) "           
    print(queryString, "what")
    #totalRange =  dateRange + nameRange 
    return [nameRange,dateRange, queryString]

def extractDatePrice(request,cursor):
    queryString = getNameDatePriceQuery(request)

    print(cursor.execute(queryString[2],queryString[1]+queryString[0]))
    priceHighLow = [[x for x in cursor.fetchall()],[]]
    currDate = [[priceHighLow[0][0][2],priceHighLow[0][0][2]],'',0,0]
    currDate[1]=priceHighLow[0][0][1]
    for x in priceHighLow[0]:
        if x[1] != currDate[1]:
            priceHighLow[1].append([x[0],currDate[1],[currDate[0][0], currDate[0][1]]])
            #print(currDate, "what")
            currDate[0][0]=x[2]
            currDate[0][1]=x[2]
            currDate[1]=x[1]
        if x[2]<currDate[0][0]:
            #print(currDate,x)

            currDate[0][0]=x[2]
        elif x[2]>currDate[0][1]:
            currDate[0][1]=x[2]
    return {'response':priceHighLow[1]}









#lim->0 |x|/2
 




#lim x-> 1/x