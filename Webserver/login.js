var emails = JSON.parse(localStorage["Emails"]);
var passwords = JSON.parse(localStorage["Passwords"]);


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
      window.location.href = 'home.html';

    }
    else {
      console.log("Login unsuccessful");
  
    }
  }  