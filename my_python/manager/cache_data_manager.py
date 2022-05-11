# Manage the datas in cache

import re

from flask import Flask, render_template, request, jsonify
import my_python.word_cloud_generation.word_cloud_generation as word_cloud_generation
import my_python.translation.translation as translation
import my_python.transcription.transcription as transcription
from urllib.request import urlretrieve
import wave, struct
import json
import js2py
import os as os

from my_python.const.lang_const import *

sample_sentences = ['Premiere Phrase', "ceci est la seconde phrase", "ho une troisieme", "petite 4eme au passage", "Puis une 5eme", "enfin une sixieme"]

displayed_sentences = {}

audio_memory = {}

sentences_rank = {}

sentences_limit = 5

audio_limit = 2

RESET_CODE = -42

###
# Init

# Init the room
def initDisplayed_sentences_room(room):
    displayed_sentences[room] = {}
    sentences_rank[room] = -1
    audio_memory[room] = []
    for language in LANGUAGES:
        displayed_sentences[room][language] = []
    return

# Reset the room
def resetDisplayed_sentences_room(room):
    return initDisplayed_sentences_room(room)


def initAudio_memory():
    audio_memory = {}
    return

def resetAudio_memory_room(room):
    audio_memory[room] = []
    return

def resetCache_room(room):
    resetAudio_memory_room(room)
    resetDisplayed_sentences_room(room)

###
# Getters

# Returns all displayed sentences
def getDisplayed_sentences():
    return displayed_sentences

# Returns all displayed sentences of the room
def getDisplayed_sentences_room(room):
    return getDisplayed_sentences()[room]

# Returns all the displayed sentences of the room in the language
def getDisplayed_sentences_room_language(room, language):
    return getDisplayed_sentences_room(room)[language]

def getDisplayed_sentences_room_language_from(room, language, from_sent):
    sent_rank = sentences_rank[room]
    displayed_sentences_scaled = displayed_sentences[room][language]
    print(sent_rank, from_sent)
    # In case of new conf
    if (sent_rank < from_sent) :
        # New conf = reset on view too
        return ([] , RESET_CODE) # return Error value

    # In case of view is very late
    elif ( from_sent - sent_rank > sentences_limit) :
        # return all the list
        return (displayed_sentences_scaled, sent_rank)

    # Standard case
    else :
        # Return the missing sentences
        return (displayed_sentences_scaled [from_sent - sent_rank:], sent_rank)


def getSound_memory():
    return audio_memory

def getSound_memory_room(room):
    return getSound_memory()[room]






###
# Setters

# Add [sentences] to the romm in the language displayed sentences list, returns the new list
def addDisplayed_sentences_room_language(room, language, sentences):
    sentences_rank[room] = sentences_rank[room] + len(sentences)
    displayed_sentences[room][language] = displayed_sentences[room][language][len(sentences)-1:] + sentences
    if (len(displayed_sentences[room][language]) > sentences_limit):
        displayed_sentences[room][language] = displayed_sentences[room][language][-sentences_limit:]
    return


def addSoundMemory(room, audioBuffer):
    # Prepare the buffer
    audioBuffer = re.sub(r'"\d*":', '', audioBuffer)
    #print(audioBuffer)
    buffer = audioBuffer.split(',')[2:-2]
    #buffer = Clear(buffer)
    # keep in memory the new datas
    for sample in buffer :
        audio_memory[room].append(sample)
    return

def removeExcess(room):
    if (len(audio_memory) > audio_limit):
        audio_memory[room] = getSound_memory_room(room)[(len(audio_memory)-audio_limit):]
    return

def getSound_memory_room(room):
    return audio_memory[room]
