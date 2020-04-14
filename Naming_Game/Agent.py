import numpy as np
import random

class Agent:
    def __init__(self, _name, _xpos, _ypos, _speed):
        self.name = _name
        self.xpos = _xpos
        self.ypos = _ypos
        self.speed = _speed
        self.vocabulary = list()
        self.num_objects = 8

        for i in range(self.num_objects):
            self.vocabulary.append([])

    
    def move(self):
        self.xpos += np.random.uniform(0,1) * self.speed
        self.ypos += np.random.uniform(0,1) * self.speed

        if self.xpos > 500:
            self.xpos = 0
        if self.xpos < 0:
            self.xpos = 500
        if self.ypos > 500:
            self.ypos = 0
        if self.ypos < 0:
            self.ypos = 500

    def speak(self, _object):
        print(self.vocabulary)
        if not self.vocabulary[_object]: #-- have no word for it yet OPEN FOR IMPROVEMENT
            word = ""
        else: 
            word = random.choice(self.vocabulary[_object])
        return word

    def invent_word(self, _object):
        syllables = ["wa", "ba", "ra", "ta", "na", "ka", "la", "pa", "za", "ma", "we", "be", "re", "te", "ne", "ke", "le", "pe", "ze", "me", "wi", "bi", "ri", "ti", "ni", "ki", "li", "pi", "zi", "mi", "wo", "bo", "ro", "to", "no", "ko", "lo", "po", "zo", "mo"]
        # _word = ""
        _word = "".join(random.sample(syllables, 3))
        self.vocabulary[_object].append(_word)
        return _word

    def interpret(self, _word):
        for i, item in enumerate(self.vocabulary):
            if _word in item:
                # print(_word, i)
                return i

        else:
            # print("no have word")
            return -1
        
    def adopt(self, _word, _object):
        self.vocabulary[_object] = []
        self.vocabulary[_object].append(_word)

    def add_word(self, _word, _object):
        self.vocabulary[_object].append(_word)