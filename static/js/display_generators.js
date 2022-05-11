const SENTENCE_SEPARATOR = "___________________";

const GenerateImg = function (path, alt, style="", onclick=null, id=null) {
  let img = "<img style='" + style + "' src=\"" + path + "\" alt='" + alt

  if (id) {
    img += "' id='" + id;
  }
  if (onclick) {
    img += "' onclick='" + onclick;
  }
  return img + "'>";
}

const GenerateExposedImg = function (name, style="weight:100%; height:100%", onclick=null, id=null) {
  return GenerateImg("../static/exposed/" + name, name, style=style, onclick=onclick, id);
}

const GenerateSentence = function (sentence, nb_sentence, pict_id=null, has_pict=true, nb_likes=null) {
  let res =  '<div id="' + getSentenceId(nb_sentence) + '"> <p> ' + sentence + ' <\p> ';

  if (nb_likes != null) {
    res += GenerateSentenceNbLikes(nb_sentence, nb_likes);
  }

  if ( has_pict) {
    res += GenerateSentenceImg(nb_sentence, pict_id, has_pict);
  }
  console.log(res);
  return res + ' <\div><div class="sentence-separator">' + SENTENCE_SEPARATOR + ' <\div>';

}

const GenerateSentenceImg = function (nb_sentence, pict_id, has_pict=true) {
  if (has_pict) {
    const onclickFunction = 'LikeSentence(' + nb_sentence + ');';
    const imgStyle = "max-width:2% !important; max-height:2% !important;";
    const imgId = getImageId(nb_sentence);
    let img = GenerateExposedImg('grey_thumbs_up.' + IMG_TYPE , style=imgStyle, onclick=onclickFunction, imgId);
    return '<p id=' + pict_id + '>' + img + ' <\p>';
  }
  return "";
}

const GenerateSentenceNbLikes = function (nb_sentence, nb_likes) {
  return '<div class="like-details">' + nb_likes + " <\div>";
}

const ChangeSentenceLikeButtonToUnlike = function (nb_sentence) {
  const imgId = getImageId(nb_sentence);
  const pict_id = getSentenceImgId(nb_sentence);
  const onclickFunction = 'UnlikeSentence(' + nb_sentence + ');';
  const imgStyle = "max-width:2% !important; max-height:2% !important;";
  document.getElementById(pict_id).innerHTML = GenerateExposedImg('green_thumbs_up.' + IMG_TYPE , style=imgStyle, onclick=onclickFunction, imgId);
}

const ChangeSentenceDislikeButtonToLike = function (nb_sentence) {
  const imgId = getImageId(nb_sentence);
  const pict_id = getSentenceImgId(nb_sentence);
  const onclickFunction = 'LikeSentence(' + nb_sentence + ');';
  const imgStyle = "max-width:2% !important; max-height:2% !important;";
  document.getElementById(pict_id).innerHTML = GenerateExposedImg('grey_thumbs_up.' + IMG_TYPE , style=imgStyle, onclick=onclickFunction, imgId);
}
