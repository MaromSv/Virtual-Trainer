var sqlite3 = require('sqlite3');

let db = new sqlite3.Database('Application/Assets/database.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Connected to the SQlite database.');
  });

//db.run('CREATE TABLE users(email text, password text)');

db.all('SELECT * FROM users', [], (err, rows) => {
  if (err) return console.error(err.message);

  rows.forEach((row) =>{
    console.log(row);
  });
});

db.close((err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Close the database connection.');
  });