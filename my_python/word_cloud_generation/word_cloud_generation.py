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

import os

from wordcloud import WordCloud, get_single_color_func

import requests

### CLOUD GENERATION METHODS

class colormap_color_func(object):
    def __init__(self, colormap):
        import matplotlib.pyplot as plt
        self.colormap = plt.cm.get_cmap(colormap)

    def __call__(self, word, font_size, position, orientation,
                 random_state=None, **kwargs):
        if random_state is None:
            random_state = Random()
        r, g, b, _ = np.maximum(0, 255 * np.array(self.colormap(
            random_state.uniform(0, 1))))
        return "rgb({:.0f}, {:.0f}, {:.0f})".format(r, g, b)

class GroupedMultiColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (colormap_color_func("viridis", 255), set(words))
            for (color, words) in color_to_words.items()]
        self.default_color_func = colormap_color_func("viridis", 60)

    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


class GroupedSingleColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]
        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

def recent_word_color_func(recent=None):
  if(recent==None) : return None

  color_to_words = {
      'blue' : tokenize_text(recent)
  }
  default_color = 'gray'

  return GroupedSingleColorFunc(color_to_words, default_color)

def tokenize_text(text):
    return [
        word
        for word in re.split("\W+", text.lower())
        if word not in stops and len(word)>1 and word.isnumeric() == False and word.isalnum() == True
    ]

 # Generate the cloud
def generate_cloud(text, recent=None, width=600, height=600):
    wordcloud = WordCloud(max_words=50, width=width, height=height,
                  stopwords=stops,
                  mode="RGBA",
                  background_color=None,
                  color_func=recent_word_color_func(recent)).generate_from_frequencies(text)

    image = wordcloud.to_image()
    return image

stops = set(stopwords.words())


### FREQUENCES TREATMENT

def get_freqDist(text, lexical_field=None, related_field=None):
  freqDist = FreqDist()
  for word in tokenize_text(text):
        freqDist[word] += 1
  return freqDist

def ponderate_freqDist(text, corpuses):
    D = 1 + len(corpuses)
    freqDist = FreqDist()
    for word in text:
        tf = 0.4+0.6*(text.freq(word)/text.freq(text.max()));#Normalized to max
        df = 1
        for corpus in corpuses:
            df += int(corpus.freq(word)>0)
        idf = math.log(D/df)
        freqDist[word] = tf*idf
    return freqDist

def stringify_freqDist(freq, occurences=20):
    return ' '.join([item for sublist in freq.most_common(occurences) for item in sublist if isinstance(item, str)])

### LEXICALS ::
def wikify(text, lang="en", threshold=0.8):
  # Prepare the URL.
  data = urllib.parse.urlencode([
    ("text", text), ("lang", lang),
    ("userKey", "qjjgwwjyilpffjyyjczftfrfmyvlcu"),
    ("pageRankSqThreshold", "%g" % threshold), ("applyPageRankSqThreshold", "true"),
    ("nTopDfValuesToIgnore", "200"), ("nWordsToIgnoreFromList", "200"),
    ("wikiDataClasses", "true"), ("wikiDataClassIds", "false"),
    ("support", "true"), ("ranges", "false"), ("minLinkFrequency", "2"),
    ("includeCosines", "false"), ("maxMentionEntropy", "3")
    ])
  url = "http://www.wikifier.org/annotate-article"
  # Call the Wikifier and read the response.
  req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
  with urllib.request.urlopen(req, timeout = 60) as f:
    response = f.read()
    response = json.loads(response.decode("utf8"))
  # Output the annotations.
  return [annotation["title"] for annotation in response["annotations"]]

def get_wikipedia_extract(title):
  r = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{title}')
  return r.json()["extract"]

def get_related_field(text):
  related_text = ""
  for annotation in wikify(text, "en"):
    related_text += get_wikipedia_extract(annotation)
  return get_freqDist(related_text)

 #### called in collab

 #Article frequences
def getArticleFrequences(article) :
    lexical_field = get_freqDist(article)
    #print(lexical_field.most_common(20))

#Domain terms
def domainTermFrequences(lexical_field):
    related_field = get_related_field(stringify_freqDist(lexical_field))
    #print(related_field.most_common(20))

#Confrence
def confrence(speech_part_1, speech_part_2, speech_part_3):
    speech = speech_part_1 + " " + speech_part_2 + " " + speech_part_3
    word_freq = get_freqDist(speech, lexical_field, related_field)
    #print(word_freq.most_common(20))

###### Callables ::
def getCloudFromTextAndLanguage(text, lang, room=-1):
    fields = get_freqDist(text)
    path = "static/exposed/word_cloud.room" + room + "." + lang + ".png"
    if os.path.exists(path):
        os.remove(path)
    generate_cloud(fields).save(path, "PNG")
