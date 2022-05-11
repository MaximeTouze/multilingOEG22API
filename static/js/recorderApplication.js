var fileReader = new FileReader();
fileReader.onload = function() {
  buffer = this.result;
  $.ajax({
    type:'POST',
    url:'/updateSound2',
    data:{
      audioBuffer:JSON.stringify(Array(new Int16Array(buffer)))
    },
    success:function()
    {
      console.log("son transmis");
    }
 });
};



var audio_context;
var recorder;



function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  __log('Media stream created.');

  // Uncomment if you want the audio to feedback directly
  //input.connect(audio_context.destination);
  //__log('Input connected to audio context destination.');

  recorder = new Recorder(input);
  console.log(recorder);
  recorder.context.onstatechange = function (evt) {
    console.log(evt);
  }
  __log('Recorder initialised.');

  startRecording();
}

function startRecording() {
  recorder && recorder.record();
  __log('Recording...');
}

function stopRecording() {
  recorder && recorder.stop();
  __log('Stopped recording.');

  if(recorder) {
    recorder.clear();
  }
}

function __log(text) {
  console.log(text);
}

const INIT = false;
function RecorderInit() {
  if (INIT) {
    startRecording();
  } else {

    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
      window.URL = window.URL || window.webkitURL;

      audio_context = new AudioContext;
      __log('Audio context set up.');
      __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
    }

    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
      __log('No live audio input: ' + e);
    });
  }
};
