// const button = document.getElementById('update_personal_info');
// if(button) {
//   button.addEventListener('click', submit_personal());
// }

function input_elements_personal_form(userid){
    first_name=document.getElementById('first_name').value;
    last_name=document.getElementById('last_name').value;
    age=document.getElementById('age').value;
    gender = get_value_personal_radio('gender');
    experience = get_value_personal_radio('experience');
    location = get_value_personal_radio('location');
    sql='INSERT INTO Personal_Form(userid, first_name, last_name, age, gender experience, location VALUES (?,?,?,?,?,?,?)';
    db.run(sql, [userid, first_name, last_name, age, gender, experience,location], function(err) {
        if (err) {
          return console.log(err.message);
        }
        console.log(`A row has been inserted`);
      });
}

function delete_elements_personal_form(userid){
    sql='DELETE FROM Personal_Form WHERE userid=? VALUES (?)';
    db.run(sql, [userid], function(err) {
        if (err) {
          return console.error(err.message);
        }
        console.log(`Row(s) deleted`);
      });
}

function get_value_personal_radio(name){
    if (document.getElementById(name).checked) {
        return document.getElementById(name).value;
    } else {
        return null; //error here
    }
}

function submit_personal(){
    // window.sqlite3InitModule().then(function(sqlite3){
    //     // The module is now loaded and the sqlite3 namespace
    //     // object was passed to this function.
    //     console.log("sqlite3:", sqlite3);
    //   });

    let db = new sqlite3.Database('Application/Assets/database.db', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
          return console.error(err.message);
        }
        console.log('Connected to the SQlite database.');
      });
  
      userid = 1;//document.getElementById('userid').value;//fix
      delete_elements_personal_form(userid);
      input_elements_personal_form(userid);
  
      db.close((err) => {
        if (err) {
          return console.error(err.message);
        }
        console.log('Close the database connection.');
      });
  }