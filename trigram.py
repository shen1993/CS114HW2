from collections import defaultdict
from languageModel import LanguageModel
import random
import bisect


class Trigram(LanguageModel):
    def __init__(self):
        self.probCounter = defaultdict(float)
        self.bigramCounter = defaultdict(float)
        self.trigramCounter = defaultdict(float)
        self.rand = random.Random()

    def train(self, trainingSentences):
        self.mu = 1.0
        self.vocabSize = 0.0
        self.accu = []
        self.accuB = []
        self.accuT = []
        self.total = 0
        self.totalB = 0
        self.totalT = 0
        for sentence in trainingSentences:
            lastWord = ""
            lastWord2 = ""
            for word in sentence:
                self.probCounter[word] += 1
                self.total += 1
                if lastWord == "" and lastWord2 == "":
                    self.trigramCounter[(LanguageModel.START, LanguageModel.START, word)] += 1
                    self.totalT += 1
                    self.bigramCounter[(LanguageModel.START, LanguageModel.START)] += 1
                    self.totalB += 1
                    lastWord = word
                elif lastWord2 == "":
                    self.trigramCounter[(LanguageModel.START, lastWord, word)] += 1
                    self.totalT += 1
                    self.bigramCounter[(LanguageModel.START, word)] += 1
                    self.totalB += 1
                    lastWord2 = lastWord
                    lastWord = word
                else:
                    self.trigramCounter[(lastWord2, lastWord, word)] += 1
                    self.totalT += 1
                    self.bigramCounter[(lastWord, word)] += 1
                    self.totalB += 1
            self.probCounter[LanguageModel.START] += 1
            self.total += 1
            self.probCounter[LanguageModel.STOP] += 1
            self.total += 1
            self.bigramCounter[(word, LanguageModel.STOP)] += 1
            self.totalB += 1
            self.trigramCounter[(lastWord, word, LanguageModel.STOP)] += 1
            self.totalT += 1

        self.probCounter[LanguageModel.UNK] += 1
        self.total += 1
        self.vocabSize = len(self.probCounter.keys())

        for (lastWord2, lastWord, word) in self.trigramCounter.keys():
            self.accuT.append(self.trigramCounter[(lastWord2, lastWord, word)] if len(self.accuT) == 0 else
                              self.accuT[-1] + self.trigramCounter[(lastWord2, lastWord, word)])

        print(len(self.probCounter))
        print(len(self.bigramCounter))
        print(len(self.trigramCounter))

    def getWordProbability(self, sentence, index):
        if index == 0:
            lastWord2 = LanguageModel.START
            lastWord = LanguageModel.START
        elif index == 1:
            lastWord2 = LanguageModel.START
            lastWord = sentence[index - 1]
        else:
            lastWord2 = sentence[index - 2]
            lastWord = sentence[index - 1]
        if index == len(sentence):
            word = LanguageModel.STOP
        else:
            word = sentence[index]
        if (lastWord2,lastWord) not in self.bigramCounter:
            return 1.0 / self.vocabSize
        elif (lastWord2,lastWord, word) in self.trigramCounter:
            return self.trigramCounter[(lastWord2,lastWord, word)] / self.bigramCounter[(lastWord2, lastWord)]
        else:
            return 0.00002

    def getVocabulary(self):
        return self.probCounter.keys()

    def generateWord(self):
        i = self.rand.randint(0, self.totalT - 1)
        index = bisect.bisect_left(self.accuT, i)
        return self.trigramCounter.keys()[index]

    def generateSentence(self):
        result = []
        for i in xrange(10):
            lastWord2 = self.generateWord()[0]
            lastWord = self.generateWord()[1]
            word = self.generateWord()[2]
            result.append(lastWord2)
            result.append(lastWord)
            result.append(word)
            if word == LanguageModel.STOP:
                break
        return result
