from collections import defaultdict
from languageModel import LanguageModel
import random
import bisect

'''
Tuan Do
'''
class Unigram (LanguageModel):
    def __init__(self):
        self.probCounter = defaultdict(float)
        self.rand = random.Random()
    
    def train(self, trainingSentences):
        self.accu = []
        
        self.total = 0
        for sentence in trainingSentences:
            for word in sentence:
                self.probCounter[word] += 1
                self.total += 1
            self.probCounter[LanguageModel.STOP] += 1
            self.total += 1

        self.probCounter[LanguageModel.UNK] += 1
        self.total += 1
            
        for word in self.probCounter.keys():
            self.accu.append(self.probCounter[word] if len(self.accu) == 0 else 
                self.accu[-1] + self.probCounter[word] )
            self.probCounter[word] /= self.total

    
    def getWordProbability(self, sentence, index):
        if index == len(sentence):
            return self.probCounter[LanguageModel.STOP]
        else:
            
            word = sentence[index]
            return self.probCounter[word] if word in self.probCounter else self.probCounter[LanguageModel.UNK]
        
    def getVocabulary(self):
        return self.probCounter.keys()

    def generateWord(self):
        i = self.rand.randint(0, self.total - 1)
        index = bisect.bisect_left( self.accu, i )
        return self.probCounter.keys()[index]
        
    def generateSentence(self):
        result = []
        for i in xrange(1000):
            word = self.generateWord()
            result.append(word)
            if word == LanguageModel.STOP:
                break
        return result