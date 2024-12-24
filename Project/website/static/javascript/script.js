var navLink = document.querySelectorAll(".nav-link")
var navLinkArray = Array.from(navLink)

for(let i=0; i < navLinkArray.length; i++){
    navLinkArray[i].addEventListener("mouseover", () => {
        navLinkArray[i].classList.add("nav-link-selected")
    })
    navLinkArray[i].addEventListener("mouseout", () => {
        navLinkArray[i].classList.remove("nav-link-selected")
    })
}

var long = document.getElementsByClassName("long")[0]
var uppercase = document.getElementsByClassName("uppercase")[0]
var lowercase = document.getElementsByClassName("lowercase")[0]
var symbol = document.getElementsByClassName("symbol")[0]
var number = document.getElementsByClassName("number")[0]

var numPattern = /[0-9]/g
var symbolPattern = /[!@#$%^&*()+-/]/g
var upperPattern = /[A-Z]/g
var lowerPattern = /[a-z]/g

function checkPassword(){
    var password = document.getElementsByClassName("password-entry")[0].value
    if(password.length > 8){
        long.src = "../static/images/check.png"
    }
    else{
        long.src = "../static/images/cancel.png"
    }
    if(numPattern.test(password)){
        number.src = "../static/images/check.png"
    }
    else{
        number.src = "../static/images/cancel.png"
    }
    if(symbolPattern.test(password)){
        symbol.src = "../static/images/check.png"
    }
    else{
        symbol.src = "../static/images/cancel.png"
    }
    if(lowerPattern.test(password)){
        lowercase.src = "../static/images/check.png"
    }
    else{
        lowercase.src = "../static/images/cancel.png"
    }
    if(upperPattern.test(password)){
        uppercase.src = "../static/images/check.png"
    }
    else{
        uppercase.src = "../static/images/cancel.png"
    }
}
