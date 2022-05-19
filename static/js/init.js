
const ENGLISH = "eng";
const FRENCH = "fr";
const SPANISH = "esp";
const ARABIAN = "ara";
// https://cloud.google.com/speech-to-text/docs/languages

// Images extentions
const IMG_TYPE = 'png';
// Languages list
const LANGUAGES = [ENGLISH, FRENCH, SPANISH, ARABIAN];
// Time before img update (ms)
const WAITING_TIME = 10000;
// Number max of sentences
const MAX_SENTENCES = 3;


//// Displays ::
const WORD_CLOUD = "word_cloud";
const SENTENCES = "sentences";

// The current language to show
let selected_language = "eng";
// the current display to show
let selected_display = WORD_CLOUD;

// the countor wich permises the display update (for pictures)
let compteur = 0;
// A boolean which permise to continue the update of the display
let continueUpdate = true;

// the link to the API back-end
//const API_BACKEND_LINK = "http://127.0.0.1:88/static/exposed/"
const API_BACKEND_LINK = "https://multiling-oeg.univ-nantes.fr/static/exposed/"
