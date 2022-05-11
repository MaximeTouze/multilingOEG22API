import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer


def wav2Vec():
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    return tokenizer, model

def transcription(tokenizer, model, input_file):
    #read the file
    speech, samplerate = sf.read(input_file)
    if len(speech.shape) > 1:
        speech = speech[:,0] + speech[:,1]

    # Sample the audio to 16khz
    if samplerate != 16000:
        speech = librosa.resample(speech, samplerate, 16000)
    input_values = tokenizer(speech, return_tensors="pt").input_values

    #take logits
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim= -1) #find the most probable word
    transcription = tokenizer.decode(predicted_ids[0])
    return transcription

def my_transcription(audio_file_path):
    return transcription(tokenizer, model, audio_file_path)

tokenizer, model = wav2Vec()
