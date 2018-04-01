console.log("signuploginHAHHA");
document.getElementById("submit").addEventListener("click", submitForm);
document.getElementById("signUpNav").addEventListener("click", signIn);
document.getElementById("loginNav").addEventListener("click", signIn);

function submitForm(){
    console.log("working");
}

function signIn(){
    document.getElementById("outPopUp").style.visibility = "visible";
}