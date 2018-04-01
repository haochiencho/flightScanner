console.log("signuploginHAHHA");
/*document.getElementById("submit").addEventListener("click", submitForm);
document.getElementById("signUpNav").addEventListener("click", signIn);
document.getElementById("loginNav").addEventListener("click", signIn);

function submitForm(){
    console.log("working");
}

function signIn(){
    document.getElementById("outPopUp").style.visibility = "visible";
}*/

$("#submit,#signUpNav,#loginNav,#outPopUp").on('click', function(e) {
    console.log("called1")
    document.getElementById("outPopUp").style.visibility = "visible";
    e.stopPropagation();
});

$(document).on('click', function (e) {
    console.log("called2")
    document.getElementById("outPopUp").style.visibility = "hidden";// Do whatever you want; the event that'd fire if the "special" element has been clicked on has been cancelled.
});
