function Find_Buddy(){
  email = "John_Smith@gmail.com"
  firstname = "John"
  lastname = "Smith"
  age = "23"
  loc = "Campus"
  gender = "Male"
  experience = "Intermediate"
  common_days = "Monday, Wednesday"


  document.getElementById("email_current_buddy").innerHTML = email;
  document.getElementById("first_name_current_buddy").innerHTML = firstname;
  document.getElementById("last_name_current_buddy").innerHTML = lastname;
  document.getElementById("age_current_buddy").innerHTML = age;
  document.getElementById("location_current_buddy").innerHTML = loc;
  document.getElementById("gender_current_buddy").innerHTML = gender;
  document.getElementById("experience_current_buddy").innerHTML = experience;
  document.getElementById("days_available_current_buddy").innerHTML = common_days;
}















// function input_elements_buddy_form(userid){
//     days_available = get_values_buddy_checkbox('days_available');
//     gender_preference = get_values_buddy_checkbox('gender_preference');
//     experience_preference = get_values_buddy_checkbox('experience_preference');
//     location_preference = get_values_buddy_checkbox('location_preference');
//     sql='INSERT INTO Buddy_Form(userid, days_available, gender_preference, experience_preference, location_preference) VALUES (?,?,?,?)';
//     db.run(sql, [userid, days_available,gender_preference,experience_preference,location_preference], function(err) {
//         if (err) {
//           return console.log(err.message);
//         }
//         console.log(`A row has been inserted`);
//       });
// }

// function delete_elements_buddy_form(userid){
//     sql='DELETE FROM Buddy_Form WHERE userid=? VALUES (?)';
//     db.run(sql, [userid], function(err) {
//         if (err) {
//           return console.error(err.message);
//         }
//         console.log(`Row(s) deleted`);
//       });
// }

// function get_values_buddy_checkbox(classname){
//     var checkedValue = null; 
//     var inputElements = document.getElementsByClassName(classname);
//     for(var i=0; inputElements[i]; ++i){
//           if(inputElements[i].checked){
//                checkedValue = inputElements[i].value;
//                break;
//           }
//     }
//     return checkedValue.toString();
// }

// function submit_buddy(){
//   var sqlite3 = require('sqlite3').verbose();

//   let db = new sqlite3.Database('Application/Assets/database.db', sqlite3.OPEN_READWRITE, (err) => {
//       if (err) {
//         return console.error(err.message);
//       }
//       console.log('Connected to the SQlite database.');
//     });

//     userid = document.getElementById('userid').value;//fix
//     delete_elements_buddy_form(userid);
//     input_elements_buddy_form(userid);

//     db.close((err) => {
//       if (err) {
//         return console.error(err.message);
//       }
//       console.log('Close the database connection.');
//     });
// }