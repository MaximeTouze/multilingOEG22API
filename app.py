from flask import Flask, render_template, request, jsonify
from urllib.request import urlretrieve
import wave, struct
import json
import js2py
import re
import os as os
import requests


import my_python.word_cloud_generation.word_cloud_generation as word_cloud_generation
import my_python.transcription.transcription as transcription
import my_python.translation.translation as translation
import my_python.api.conf_manager as ConfManager
import my_python.manager.cache_data_manager as CacheDataManager
import my_python.const.lang_const as LangConst

API_BACKEND_LINK = "http://127.0.0.1:88"
#API_BACKEND_LINK = "https://multiling-oeg.univ-nantes.fr/"

app = Flask(__name__, template_folder='templates')
app.debug = True


#app.run(ssl_context="adhoc")

## The app's html view ::

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/recorderLook')
def recorderLook():
    return render_template('RecorderFrontTesting.html')


## The app's solution

@app.route("/update", methods=['POST'])
def update():
    text = request.form['text']
    language = request.form['lang']
    word_cloud_generation.getCloudFromTextAndLanguage(text, language)
    return render_template('record.html')

@app.route("/updateSound2", methods=['POST'])
def updateSound2():
    #print('called', request.form)
    audioBuffer = request.form.get('audioBuffer')
    room = int(request.form.get('room'))
    lang = ConfManager.getLangFromRoom(room)


    if os.path.exists("current.wav"):
        os.remove("current.wav")


    #print(audioBuffer)
    # Prepare wave file
    file_path = "current.wav"
    file = wave.open(file_path, "wb")
    file.setnchannels(1)
    sampleRate = 44100.0*2 # hertz
    file.setsampwidth(2)
    file.setframerate(sampleRate)

    CacheDataManager.addSoundMemory(room, audioBuffer)
    audio_memory = CacheDataManager.getSound_memory_room(room)

    ## Create the wave with the past memory
    #for sound_part in audio_memory:
    #    for item in sound_part:
    #        file.writeframesraw( struct.pack('<h', int(item)) )

    # Prepare the buffer
    #audioBuffer = re.sub(r'"\d*":', '', audioBuffer)
    #print(audioBuffer)
    #buffer = audioBuffer.split(',')[2:-2]
    #buffer = Clear(buffer)
    #memory = []
    for sample in audio_memory:
        data = struct.pack('<h', int(sample))
    #    memory.append(sample)
        file.writeframesraw( struct.pack('<h', int(sample)) )


    print('============ Recording getted ===========')
    # Don t forgot to close
    file.close()
    (trans, time) = transcription.process_wav_google_cloud(file_path, language=LangConst.LANGUAGES_MATCHER[lang][LangConst.TRANS], target=LangConst.LANGUAGES_MATCHER[lang][LangConst.TRAD])
    print(trans)
    print(type(trans))
    sentences = trans.split('\n')
    CacheDataManager.addDisplayed_sentences_room_language(room, lang, sentences)
    # remove excess from sound cache
    if (len(sentences) >= 2):
        CacheDataManager.removeExcess(room)

    # For each other language than the spoken one
    for language in LangConst.LANGUAGES:

        # traduction for each language except the spoken one
        if (lang != language):
            trad_lang = LangConst.LANGUAGES_MATCHER[language][LangConst.TRAD]
            # For each sentence
            for sentence in sentences:
                # translate & add the sentence to the displayed_sentences list
                trad_sentence = GoogleTranslator(source='auto').translate(sentence)
                addDisplayed_sentences_room_language(room, lang, trad_sentence)
                word_cloud_generation.getCloudFromTextAndLanguage(trad_sentence, lang, room)
        else :
            for sentence in sentences:
                word_cloud_generation.getCloudFromTextAndLanguage(sentence, lang, room)

    #word_cloud_generation.getCloudFromTextAndLanguage(text, language)
    return render_template('test.html')



@app.route("/translate", methods=['POST'])
def translate():
    #translation.translate_text("hi")
    print(request.form.get('text'))
    return render_template('record.html')




@app.route("/sentences", methods=['GET'])
def sentences():
    print(request.form, request.args)
    num_sentence = int(request.args.get('nb_sentence'))
    room = int(request.args.get('room'))
    lang = request.args.get('lang')

    sentences = CacheDataManager.getDisplayed_sentences_room_language_from(room, lang, num_sentence)
    return jsonify({'sentences': sentences})



########### Likes ###############

@app.route("/likeSentence", methods=['POST'])
def LikeSentence():
    likeSystem.LikeSentence(request)
    return render_template('view.html')

@app.route("/UnlikeSentence", methods=['POST'])
def UnlikeSentence():
    likeSystem.UnlikeSentence(request)
    return render_template('view.html')

################################


@app.route("/mostly_liked_sentences", methods=['GET'])
def Mostly_liked_sentences_api():
    room = int(request.args.get('room'))
    return requests.post(API_BACKEND_LINK, data = request)

@app.route("/startConf", methods=['POST'])
def startConf():
    print (request)
    print(request.args)
    print (request.form)
    room = int(request.form.get('room'))
    lang = request.form.get('lang')
    ConfManager.startConf(room, lang)
    return render_template('RecorderFrontTesting.html')

@app.route("/stopConf", methods=['POST'])
def stopConf():
    room = int(request.form.get('room'))
    ConfManager.setConf_questions_state(room)
    return render_template('RecorderFrontTesting.html')

@app.route("/endConf", methods=['POST'])
def endConf():
    room = int(request.form.get('room'))
    ConfManager.endConf(room)
    return render_template('RecorderFrontTesting.html')


def Clear(list):
    return [x for x in list if x != 0]

if __name__== '__main__':
    app.run()
