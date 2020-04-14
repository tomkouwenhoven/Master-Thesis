import random

class Game:
    def __init__(self, _speaker, _hearer):
        self.speaker = _speaker
        self.hearer = _hearer
        self.success = 0
        self.alignment_success = 0
        self.word_invented = ""

    def play(self):
        self.success = 0
        self.alignment_succes = 0
        current_object = random.randint(0, self.speaker.num_objects - 1)
        word = self.speaker.speak(current_object)
        # print(word)

        if word == "":
            word = self.speaker.invent_word(current_object)
            self.word_invented = word
        
        interpreted_object = self.hearer.interpret(word)

        if interpreted_object == current_object:
            if (len(self.speaker.vocabulary[current_object]) == 1) and (len(self.hearer.vocabulary[current_object]) == 1):
                self.alignment_success = 1
            self.success = 1

            self.speaker.adopt(word, current_object)
            self.hearer.adopt(word, current_object)
        else:
            self.hearer.add_word(word, current_object)

