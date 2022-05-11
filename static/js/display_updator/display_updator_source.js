// Show the most liked sentences
function showMostlyLikedSentences() {
  room = getValFromRoomForm();
  console.log(room);
  $.ajax({
    type:'GET',
    url:'/mostly_liked_sentences',
    data:{
      'room':room
    },
    success:function(response)
    {
      console.log("rsp", response);
      const elt = document.getElementById('param-cell');
      const memory = elt.innerHTML;
      elt.innerHTML = "";
      let liked_sentences = response.liked_sentences;
      console.warn(liked_sentences);
      for (var i = 0; i< LANGUAGES.length; i++) {
        let current_liked_sentence = liked_sentences[LANGUAGES[i]];
        let current_sentence = current_liked_sentence.sentence;
        let current_nb_likes = LANGUAGES[i] + ' ' + current_liked_sentence.nb_likes;
        elt.innerHTML += GenerateSentence(current_sentence,  i, getSentenceImgId(i, true), false, current_nb_likes);
      }
      elt.innerHTML += memory;
    }
  });
}

// Function wiche permises to change the word cloud's language atomatically on each refreshing
async function AutoLanguageUpdator() {
      while (continueUpdate) {
        for (language in LANGUAGES) {
          if( ! continueUpdate) break;
          selected_language = LANGUAGES[language];
          display_update();
          await sleep(WAITING_TIME);
        }
      }
}

// Updates the display part
async function display_update () {
  //Ongoing on healthfull basis

  if (!updateUngoing || previous_display != selected_display) {
    updateUngoing = true;

    if(selected_display == WORD_CLOUD) {
      previous_display = WORD_CLOUD;
      wordCloud_update();
    }

   updateUngoing = false;
  }
}
