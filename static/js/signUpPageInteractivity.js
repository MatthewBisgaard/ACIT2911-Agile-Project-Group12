let passwordLengthMet = false;
let passwordMatches = false;

const checkAllRequirements = () => {
    const signUp = document.getElementById("submit");
    if (passwordLengthMet && passwordMatches){ 
        signUp.disabled = false;
    } else{
        signUp.disabled = true;    
    }
}

const checkMatch = () => {
    const confirm = document.querySelector("#confirm");
    const passwd = document.querySelector("#password");
    passwd.addEventListener("keyup", checkMatch);
    if (passwd.value === confirm.value) {
        passwordMatches = true;
        confirm.style = ""
        passwd.style = ""
    } else {
        passwordMatches = false;
        confirm.style = "background-color: red"
        passwd.style = "background-color: red"
    }
}

const checkPasswordLength = (passwordBox) => {
    // Currently only 8+ characters. This is terrible and I will (probably not) redo it
    const requirements = document.getElementById("password-requirements");
    if (passwordBox.target.value.length > 8){
        passwordLengthMet = true;
        requirements.style = "color: green;";
    } else {
        passwordLengthMet = false;
        requirements.style = "";
    }
}

const enterKeyHandler = (keyPressed) => {
    if (keyPressed.key === "Enter") {
        document.getElementById("submit").click()
    }
}

const init = () => {
    document.getElementById("password").addEventListener("keyup", checkPasswordLength);
    document.getElementById("confirm").addEventListener("keyup", checkMatch);
    setInterval(checkAllRequirements, 250)

    for (const inputOf of document.querySelectorAll("input.text")){ 
        inputOf.addEventListener("keypress", enterKeyHandler);
    }
}

window.addEventListener("load", init);