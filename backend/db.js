const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'Loverain123!',
  database: 'my_database', 
  multipleStatements: true 
});

connection.connect((err) => {
  if (err) {
    console.error('數據庫連接失敗：', err.stack);
    return;
  }
  console.log('已連接到數據庫');
});

module.exports = connection;
