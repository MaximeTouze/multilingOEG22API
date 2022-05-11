import torch
import os
import io

from IPython.display import Image, Audio

from pydub import AudioSegment
from pydub.silence import split_on_silence

import time

import speech_recognition as sr
from google.cloud import speech
from transformers import MBart50Tokenizer, SpeechEncoderDecoderModel, Wav2Vec2FeatureExtractor, Wav2Vec2Processor, Wav2Vec2ForCTC

from deep_translator import GoogleTranslator

import string
from jiwer import wer, mer, wil

import matplotlib.pyplot as plt
import numpy as np

import urllib.parse, urllib.request, json

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
nltk.download('punkt')
nltk.download('stopwords')

import numpy as np
import random as Random
import re
import math

from wordcloud import WordCloud, get_single_color_func

import requests

from my_python.const.lang_const import *

credential_path = "./my_python/credentials/speechtotextapi.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

client = speech.SpeechClient()

def preprocess_text(text):
    text = text.replace("-", " ")
    text = text.replace("'", " ")
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def wav_to_chunks(path):
    sound = AudioSegment.from_wav(path).set_frame_rate(8000)

    chunks = split_on_silence(sound,
    min_silence_len = 750,
    silence_thresh = -40,
    keep_silence = 500,)

    return chunks

def process_wav_google_cloud(path, language="en-US", target=""):
    start_time = time.time()
    transcription = ""

    for audio_chunk in wav_to_chunks(path):
        start_time_chunk = time.time()

        f = io.BytesIO()
        f = audio_chunk.export(f, format="wav")
        content = f.read()
        f.close()
        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz = 8000, # 16000 won't work use 8000
            language_code = language,
        )
        response  = client.recognize(config=config, audio=audio)

        if (response.results != []):
            line = response.results[0].alternatives[0].transcript

        else :
            line = ""
            line = GoogleTranslator(source='auto', target=target).translate(line)

        transcription += line + "\n"
        print(f"{line} - {time.time() - start_time_chunk} seconds")
    total_time = time.time() - start_time
    return transcription, total_time
