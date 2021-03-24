
const { app, BrowserWindow } = require("electron")

function toSignUp(){
  window.location.href="signup.html";
}

app.on("ready", createWindow)