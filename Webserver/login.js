var emails = JSON.parse(localStorage["userEmails"]);
var passwords = JSON.parse(localStorage["userPasswords"]);
var firstnames = JSON.parse(localStorage["userFirstNames"]);
var lastnames = JSON.parse(localStorage["userLastNames"]);
var ages = JSON.parse(localStorage["userAges"]);
var locations = JSON.parse(localStorage["userLocations"]);
var genders = JSON.parse(localStorage["userGenders"]);
var experiences = JSON.parse(localStorage["userExperiences"]);

//button listener for login
const loginbtn = document.getElementById('loginbutton');
if(loginbtn) {
  loginbtn.addEventListener('click', login);
}

//login
function login(){
    var email = document.getElementById("loginemail").value;
    var password =document.getElementById("loginpw").value;  
    var correctEmail = false;
    var correctPw = false;
  
    for (let i = 0; i <= emails.length; i++) {
      console.log("current email = " + email);
      console.log("Email array:" + emails);
  
      console.log("current email comparing to = " + emails.at(i));
  
      if(email == emails.at(i)){
        correctEmail = true;
        break;
      }
    }
  
    for (let i = 0; i <= passwords.length; i++) {
      console.log("current password = " + password);
      console.log("current password comparing to = " + passwords.at(i));
  
      if(password == passwords.at(i)){
        correctPw = true;
        break;
      }
    }
  
    console.log("correctEmail value = " + correctEmail + "correctPw value = " + correctPw);
  
    if(correctEmail == true && correctPw == true){
      console.log("Login successful");
      localStorage.setItem("email", email);
      localStorage.setItem("firstname", firstnames.at(0));
      localStorage.setItem("lastname", lastnames.at(0));
      localStorage.setItem("age", ages.at(0));
      localStorage.setItem("loc", locations.at(0));
      localStorage.setItem("gender", genders.at(0));
      localStorage.setItem("experience", experiences.at(0));



      window.location.href = 'home.html';

    }
    else {
      console.log("Login unsuccessful");
  
    }
  }  