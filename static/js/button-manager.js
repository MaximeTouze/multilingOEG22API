/** Common methods */

const ChangeSelectedButtonFunction = function (old, new_) {
  document.getElementById(old + '-button').className =
      document.getElementById(old + '-button').className[0] + " basic_color_cell";

  document.getElementById(new_ + '-button').className =
      document.getElementById(new_ + '-button').className[0] + " selected_color_cell";
}

/**
    Language buttons managment (all the first row ones)
*/

const LanguagesButtonsFunction = function (language) {
  ChangeSelectedButtonFunction(selected_language, language);

  selected_language = language;
  display_update();
}

/**
    Display buttons managment
*/

const DisplaysButtonsFunction = function (display) {
  ChangeSelectedButtonFunction(selected_display, display);

  selected_display = display;
  display_update();
}

const LikeSentence = function (sentence_num) {
  ChangeSentenceLikeButtonToUnlike(sentence_num);
  $.ajax({
    type:'POST',
    url:'/likeSentence',
    data:{
      'nb_sentence':sentence_num,
      'lang':selected_language
    },
    success:function(response) {}
 });
}

const UnlikeSentence = function (sentence_num) {
  ChangeSentenceUnlikeButtonToLike(sentence_num);
  $.ajax({
    type:'POST',
    url:'/UnlikeSentence',
    data:{
      'nb_sentence':sentence_num,
      'lang':selected_language
    },
    success:function(response) {}
 });
}
