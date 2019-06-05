from collections import defaultdict
from languageModel import LanguageModel
import random
import bisect


class Bigram(LanguageModel):
    def __init__(self):
        self.probCounter = defaultdict(float)
        self.bigramCounter = defaultdict(float)
        self.rand = random.Random()

    def train(self, trainingSentences):
        self.mu = 1.0
        self.vocabSize = 0.0
        self.accu = []
        self.accuB = []
        self.total = 0
        self.totalB = 0
        for sentence in trainingSentences:
            lastWord = ""
            for word in sentence:
                self.probCounter[word] += 1
                self.total += 1
                if lastWord == "":
                    self.bigramCounter[(LanguageModel.START, word)] += 1
                    self.totalB += 1
                    lastWord = word
                else:
                    self.bigramCounter[(lastWord, word)] += 1
                    self.totalB += 1
            self.probCounter[LanguageModel.START] += 1
            self.total += 1
            self.probCounter[LanguageModel.STOP] += 1
            self.total += 1
            self.bigramCounter[(word, LanguageModel.STOP)] += 1
            self.totalB += 1

        self.probCounter[LanguageModel.UNK] += 1
        self.total += 1
        self.vocabSize = len(self.probCounter.keys())


        for (lastWord, word) in self.bigramCounter.keys():
            self.accuB.append(self.bigramCounter[(lastWord, word)] if len(self.accuB) == 0 else
                              self.accuB[-1] + self.bigramCounter[(lastWord, word)])

        print(len(self.probCounter))
        print(len(self.bigramCounter))

    def getWordProbability(self, sentence, index):
        if index == 0:
            lastWord = LanguageModel.START
        else:
            lastWord = sentence[index - 1]
        if index == len(sentence):
            word = LanguageModel.STOP
        else:
            word = sentence[index]
        if lastWord not in self.probCounter:
            return 1.0 / self.vocabSize
        elif (lastWord, word) in self.bigramCounter:
            return (self.bigramCounter[(lastWord, word)] + self.mu) / (
            self.probCounter[lastWord] + (self.vocabSize * self.mu))
        else:
            return self.mu / (self.probCounter[lastWord] + (self.vocabSize * self.mu))

    def getVocabulary(self):
        return self.probCounter.keys()

    def generateWord(self):  # returns a tuple
        # self.reduced_d = {(lw, w): v for (lw, w), v in self.bigramCounter.items() if lw == lastWord}
        #
        # if self.reduced_d:
        #     self.accu = []
        #     for (lastWord, word) in self.reduced_d.keys():
        #         self.accu.append(self.reduced_d[(lastWord, word)] if len(self.accu) == 0 else
        #                          self.accu[-1] + self.reduced_d[(lastWord, word)])
        #
        #     i = self.rand.randint(0, self.accu[-1] - 1)
        #     index = bisect.bisect_left(self.accu, i)
        #     return self.reduced_d.keys()[index]
        # else:
        #     self.accu = []
        #     for (lastWord, word) in self.bigramCounter.keys():
        #         self.accu.append(self.bigramCounter[(lastWord, word)] if len(self.accu) == 0 else
        #                          self.accu[-1] + self.bigramCounter[(lastWord, word)])
        #
        #     i = self.rand.randint(0, self.total - 1)
        #     index = bisect.bisect_left(self.accu, i)
        #     return self.bigramCounter.keys()[index]
        i = self.rand.randint(0, self.totalB - 1)
        index = bisect.bisect_left(self.accuB, i)
        return self.bigramCounter.keys()[index]

    def generateSentence(self):
        # result = []
        # for i in xrange(1000):
        #     if i == 0:
        #         word = self.generateWord(LanguageModel.START)[1]
        #     else:
        #         word = self.generateWord(result[-1])[1]
        #     result.append(word)
        #     if word == LanguageModel.STOP:
        #         break
        # return result
        result = []
        for i in xrange(10):
            lastWord = self.generateWord()[0]
            word = self.generateWord()[1]
            result.append(lastWord)
            result.append(word)
            if word == LanguageModel.STOP:
                break
        return result
