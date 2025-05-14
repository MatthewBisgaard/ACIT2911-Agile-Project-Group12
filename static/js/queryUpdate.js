// Found on https://stackoverflow.com/questions/5999118/how-can-i-add-or-update-a-query-string-parameter
// Too good not to sue (with a few changes)
const updateQueryStringParameter = (uri, key, value) => {
  const re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  const separator = uri.indexOf('?') !== -1 ? "&" : "?";
  if (uri.match(re)) {
    return uri.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri + separator + key + "=" + value;
  }
}

const toggleCompleteShow = () => {
  
}

const load_url = location.toString()

// Call this
const updateURL = (key, value) => location = updateQueryStringParameter(load_url, key, value);
window.addEventListener('load', () => {
  if (load_url.includes("show=true")){
    document.getElementById
  }
})