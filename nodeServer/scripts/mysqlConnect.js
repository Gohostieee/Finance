
require('dotenv').config({path:"src/secret.env"})

const mysql = require('mysql');
dbKeys=JSON.parse(process.env.googleCloud)

const con = mysql.createConnection({
  user:dbKeys["user"],password:dbKeys["password"],host:dbKeys["host"],database:dbKeys["dbName"]
});
con.connect()
function myQuery(cursor,table,val){
  cursor.query("")
}
exports.sql = con