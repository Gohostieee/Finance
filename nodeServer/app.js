const express = require('express');
const app = express()
const connection = require("./scripts/mysqlConnect")
const cursor = connection.sql

cursor.query("select * from apiKeys", ( result) =>{console.log(result)})




console.log("through")








function getDatesInRange(startDate, endDate) {
  startDate = new Date(startDate)
  const date = new Date(startDate.getTime());
  let count = 0
  endDate = new Date(endDate)

  const dates = [];

  while (date <= endDate) {
  	let currDate = new Date(date)
  	count+=1
  	const year = currDate.getFullYear()
  	let month = currDate.getMonth()+1
  	let day = currDate.getDate()
  	console.log(day,month)
  	if (day<10){day=`0%{day}`}
  	if (month<10){month='0'+month;console.log("uwu")}
  	let datesVar = `${year}-${month}-${day}`
    dates.push(datesVar);
    console.log(dates)
    date.setDate(date.getDate() + 1);
  }
  console.log("final var",dates)
  return dates
}
function dateFormatter(date){
	let start,mid,end
	for(let x = 0;  x < 3;x++){
		if(parseint(date.split('-')[x])<10 & date.split('-')[x].length<4){
			if(x>0){start = date.split('-')[x-1]}
			mid='0' + date.split('-')[x]
			if(x<2){end = date.split('x')}
		}
	}
}

app.get("/", (req,res)=>{
	res.send("connection recieved")
})
 
app.get("/api", (req, res) =>{
	const key = req.query.apiKey;
	const quer = req.query.quer;
	 cursor.query('select * from apiKeys  where apiKey = ?', [key], (err,bogus,fields)=>{
			console.log(bogus)
	if (bogus == null){
		res.send("api key not found")
	}else{
		switch(quer){
			case "daily":
			let dates = [req.query.start,req.query.end]
			let categories = req.query.categories
			let categoriesList = []
			console.log(dates)
			let count;
			for(let x = 0;x<categories.split(', ').length;x++){
					categoriesList.push(categories.split(',')[x])
					console.log("nada")
			}
			console.log("what",categoriesList, categories)
			
			dates = (getDatesInRange(dates[0],dates[1]))
			console.log(cursor.query('select ?? from coinPriceData where date in (?)',[categoriesList,dates],(e,r,f)=>{
				res.send(r)
			}))
			
			break;
		}
	}


	})
})

app.listen(8080)