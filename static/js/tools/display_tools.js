// Returns the htmml id of the sentence, need the sentence's number as parameter
function getImageId (nb) {
  return "sentence-thumb-" + nb;
}

// Returns the htmml id of the sentence, need the sentence's number as parameter
function getSentenceId(num) {
  return "sentence-num-" + num;
}

// Returns the html id of the sentence's picture, need the sentence's number as param
function getSentenceImgId (number) {
  return "sentence" + number + "_pict"
}

// Classical sleep function
function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}

// remove the DOM element
function removeElement (elem) {
  elem.parentNode.removeChild(elem);
}
