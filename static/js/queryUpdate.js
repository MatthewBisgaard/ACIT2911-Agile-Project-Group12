// Originally ound on https://stackoverflow.com/questions/5999118/how-can-i-add-or-update-a-query-string-parameter
// I have made many tweaks to better serve out purposes
const updateQueryStringParameter = (uri, key, value) => {
  const re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  const separator = uri.indexOf('?') !== -1 ? "&" : "?";


  if (value === undefined){ // new clears if value is undefined
    return uri.replace(re, '$1' + "$2");
  } else if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  } else {
    return uri + separator + key + "=" + value;
  }
}

const load_url = location.toString()

// Wrapper to immediately update the URL
const updateURL = (key, value) => location = updateQueryStringParameter(load_url, key, value);

// Toggles showing complete
const toggleCompleteShow = () => {
  updateURL("show", (load_url.includes("show=true")? "false":"true"))
}

// Makes the show/hide completed button look correct
window.addEventListener('load', () => {
  const toggleButton = document.getElementById("toggle-completed");
  toggleButton.innerText = (load_url.includes("show=true")? "Hide":"Show")+" Completed";
})