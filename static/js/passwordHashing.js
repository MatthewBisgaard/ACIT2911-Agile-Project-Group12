
const userExists = async (callback) => {
    let username = document.querySelector("#username").value;
    const req = await fetch(`/auth/exists/${username}`, { method: 'GET'})
    if (req.ok){
        callback(undefined, true);
    } else if (req.status==404) {
        callback(undefined, false)
    } else{
        callback(Error("Code unknown"))
    }
}

const hashPasswdThenSubmit = async (err, issueProceeding) => {
    if (err || issueProceeding) return;
    // SOme code here comes from mozilla
    const passwd8 = new TextEncoder().encode(`${document.getElementById("password").value}`);
    const hashArrayBuffer = await window.crypto.subtle.digest("SHA-256", passwd8);
    const hashArray = Array.from(new Uint8Array(hashArrayBuffer)); // convert buffer to byte array
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join(""); // convert bytes to hex string
    
    document.getElementById("hashpasswd").value = hashHex;
    document.getElementById("hiddenusername").value = document.getElementById("username").value;


    document.getElementById("main-form").submit()
}

const startLogin = () => hashPasswdThenSubmit(undefined, false);
const startSignup = () => userExists(hashPasswdThenSubmit);
const enterKeyPress = (event) => { if (event.key == "Enter") document.getElementById("submit").click() };

window.addEventListener('load', () => {
    document.getElementById("username").addEventListener('keypress', enterKeyPress)
    document.getElementById("password").addEventListener('keypress', enterKeyPress)
})