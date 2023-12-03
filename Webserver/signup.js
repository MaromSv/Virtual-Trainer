const button = document.getElementById('createAccButton');
if(button) {
  button.addEventListener('click', createAcc);
}

function myFunction() {
  var str = "hoi";
  console.log(str);
}
// (document.getElementById('email').value

function createAcc() {
  var sqlite3 = require('sqlite3');

  //connect DB
  let db = new sqlite3.Database('Application/Assets/database.db', sqlite3.OPEN_READWRITE, (err) => {
      if (err) {
        return console.error(err.message);
      }
      console.log('Connected to the SQlite database.');
  });

  //get email and password and insert into db
  document.getElementById("email").value;
  console.log("email: ", email);
  console.log("password: ", password);

  document.getElementById("password").value;
  db.run('INSERT INTO users(email,password) VALUES(?,?)', [email,password], function(err){
      if (err) {
          return console.log(err.message);
        }
        // get the last insert id
        console.log(`A row has been inserted with rowid ${this.lastID}`);
  
    
})

  //close db
  db.close((err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Close the database connection.');
  });

};


