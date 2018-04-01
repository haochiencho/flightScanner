console.log("signuploginHAHHA");

$("#submit,#signUpNav,#loginNav,#outPopUp").on('click', function(e) {
    document.getElementById("outPopUp").style.visibility = "visible";
    e.stopPropagation();
});

$(document).on('click', function (e) {
    document.getElementById("outPopUp").style.visibility = "hidden";// Do whatever you want; the event that'd fire if the "special" element has been clicked on has been cancelled.
});
