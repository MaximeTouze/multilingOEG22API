# Manage conf status

from my_python.manager.cache_data_manager import initDisplayed_sentences_room, resetCache_room


# Consts
CONFRENCE_ON = 1
CONFRENCE_QUESTIONS = 0
CONFRENCE_OFF = -1

# Globals
confrence_status = {}
confrence_lang = {}


def getConfStaus(room):
    return confrence_status[room]

def startConf(room, lang):
    confrence_status[room] = CONFRENCE_ON
    confrence_lang[room] = lang
    initDisplayed_sentences_room(room)
    return

def setConf_questions_state(room):
    confrence_status[room] = CONFRENCE_QUESTIONS
    return

def endConf(room):
    confrence_status[room] = CONFRENCE_OFF
    confrence_lang[room] = ''
    resetCache_room(room)
    return

def getLangFromRoom(room):
    return confrence_lang[room]
