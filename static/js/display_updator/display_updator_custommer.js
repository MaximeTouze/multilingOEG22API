// MOCKS
room = 1
//

function updateSentence () {
  $.ajax({
    type:'GET',
    url:'/sentences',
    data:{
      'nb_sentence':sentences.length,
      'room':room,
      'lang':selected_language
    },
    success:function(response)
    {
      const elt = document.getElementById('displayPanel');
      const sentences_ = response.sentences;

      for (var i = 0; i < response.sentences.length; i++) {
        sentence_rank = sentences.length + i;
        if (!document.getElementById(getSentenceId(sentence_rank))) {
          current_nb_sentence ++;
          elt.innerHTML += GenerateSentence(sentences_[i],  sentence_rank, getSentenceImgId(sentence_rank, true));
          if (current_nb_sentence > MAX_SENTENCES) {
            removeExtraSentence(sentence_rank);
          }
        }
      }
      sentences = sentences.concat(sentences_);
    }
 });
}

// Updates the display part
async function display_update () {
  //Ongoing on healthfull basis

  if (!updateUngoing || previous_display != selected_display) {
    updateUngoing = true;

    if(previous_display != selected_display) {
      document.getElementById('displayPanel').innerHTML = "";
      if(selected_display == SENTENCES ) {
        loadSentences();
      }
    }

    if(selected_display == WORD_CLOUD) {
      previous_display = WORD_CLOUD;
      wordCloud_update();

    } else if (selected_display == SENTENCES) {
      previous_display = SENTENCES;
      updateSentence();
   }
   updateUngoing = false;
  }
}



// remove the sentence if there are more than the MAX_SENTENCES limit
function removeExtraSentence(last_sentence_index) {
  // We count from 1, but ranks are from 0
  removeElement(
    document.getElementById(
      getSentenceId(last_sentence_index - MAX_SENTENCES)
    )
  );
  current_nb_sentence --;
}
