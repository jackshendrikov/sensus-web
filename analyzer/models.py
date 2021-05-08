import os

from django.conf import settings
from django.db import models
from re import match
from nltk.tokenize import RegexpTokenizer
from tensorflow.keras.models import load_model

from sensus.settings import WordVec, graph

import pymorphy2
import numpy as np


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
        super(Document, self).delete(*args, **kwargs)


class Sentence(models.Model):

    def __init__(self, sent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sent = sent

    STOP_WORDS = set(line.strip() for line in open('model/stopwords_ua.txt', mode="r", encoding="utf-8"))
    MORPH = pymorphy2.MorphAnalyzer(lang='uk')
    MAX_SEQ_LEN = 100

    @staticmethod
    def regex_tokenizer(sentence):
        return RegexpTokenizer(r'\w+').tokenize(sentence)

    @staticmethod
    def stopwords_elimination(stop_words, sentence):
        return [w for w in sentence if w not in stop_words]

    @staticmethod
    def lemmatize_words(morph, words):
        return [morph.parse(word)[0].normal_form for word in words]

    def irr_words_elimination(self, words):
        words_list = self.regex_tokenizer(words)
        words_list = [item.lower() for item in words_list]
        print(words_list)

        for word in words_list:
            if bool(match(r"[a-zA-Z]", word)) or word.isdigit() or len(word) <= 3:
                words_list.remove(word)
        print(words_list)
        return words_list

    def data_preparation(self):
        words_list = self.regex_tokenizer(self.sent)
        words_list = self.stopwords_elimination(self.STOP_WORDS, words_list)
        words_list = self.lemmatize_words(self.MORPH, words_list)
        words_list = self.irr_words_elimination(' '.join(words_list))
        return words_list

    @staticmethod
    def sent_embed(words):
        sent_embed = []
        words_list = list(WordVec.vocab)

        for word in words:
            if word not in words_list:
                sent_embed.append([0] * 300)
            elif word in words_list:
                sent_embed.append(WordVec[word])

        return sent_embed

    @staticmethod
    def fix_sentence_len(sentence, length):
        if len(sentence) > length:
            sentence = sentence[:length]
        elif len(sentence) < length:
            for i in range(length - len(sentence)):
                zeros = [0] * 300
                sentence.append(zeros)
        return sentence

    def prediction(self):
        data = self.data_preparation()
        print(data)
        data = self.sent_embed(data)
        data = self.fix_sentence_len(data, self.MAX_SEQ_LEN)
        data = np.reshape(data, (1, 100, 300))

        with graph.as_default():
            model = load_model("model/LSTM-CNN-Model.h5")  # load model
            print(model.predict(np.array(data)))
            return model.predict(np.array(data))
