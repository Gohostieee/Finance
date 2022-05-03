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

def _dateRange(start,end):
	start = [int(x) for x in start.split("-")]
	end = [int(x) for x in end.split("-")]	

	start = date(start[0],start[1],start[2]) 
	end = date(end[0],end[1],end[2])    # perhaps date.now()

	delta = end - start   # returns timedelta

	return [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
		
