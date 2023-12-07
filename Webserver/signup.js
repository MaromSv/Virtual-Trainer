//Initialization of arrays
var userEmail = [];
var userPw = [];
var userPw2 = [];
var userFirstName = [];
var userLastName = [];
var userAge = [];
var locations = [];
var genders = []; 
var experiences = [];

//button listener for signup
const signupbtn = document.getElementById('createAccButton');
if(signupbtn) {
  signupbtn.addEventListener('click', createAcc);
}


//acc creation
function createAcc() {

//get values from form
var email = document.getElementById("email").value;
var password =document.getElementById("password").value;
var password2 = document.getElementById("password2").value;
var firstname = document.getElementById("first_name").value;
var lastname = document.getElementById("last_name").value
var age = document.getElementById("age").value;
var location = document.querySelector('input[name="location"]:checked').value;
var gender = document.querySelector('input[name="gender"]:checked').value;
var experience = document.querySelector('input[name="experience"]:checked').value;



//verify passwords
if(password == password2){
  userEmail.push(email);
  userPw.push(password);
  userPw2.push(password2);
  userFirstName.push(firstname);
  userLastName.push(lastname);
  userAge.push(age);
  locations.push(location);
  genders.push(gender);
  experiences.push(experience);
} else {
  console.log("treis elies");
}



console.log("Email array:" + userEmail);
console.log("Password array:" + userPw);

localStorage["Emails"] = JSON.stringify(userEmail);
localStorage["Passwords"] = JSON.stringify(userPw);
localStorage["userFirstNames"] = JSON.stringify(userFirstName);
localStorage["userLastNames"] = JSON.stringify(userLastName);
localStorage["userAge"] = JSON.stringify(userAge);
localStorage["locations"] = JSON.stringify(locations);
localStorage["genders"] = JSON.stringify(genders);
localStorage["experiences"] = JSON.stringify(experiences);
}
 
