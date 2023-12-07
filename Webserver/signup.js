import sqlite3 from "sqlite3";
import { open } from "sqlite";

const button = document.getElementById('createAccButton');
if(button) {
  button.addEventListener('click', createAcc);

}

const dbPromise = open({
  filename: "data.db",
  driver: sqlite3.Database,
});

app.get("/", async (req, res) => {
  const db = await dbPromise;
  const users = await db.all("SELECT * FROM users;");
  res.render("home", { users });
});

function createAcc() {
var email = document.getElementById("email").value;
var password =document.getElementById("password").value;
console.log("email: ", email);
console.log("password: ", password); 


}
 
  




