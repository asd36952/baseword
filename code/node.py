import numpy as np

WN_DIR = "/home/asd36952/baseword/WordNet-3.0/"
#WN_DATA_TYPE = ["verb", "noun", "adv", "adj"]
WN_DATA_TYPE = ["verb", "adv", "adj"]

p_drop = 0

class Word_Dictionary():
    def __init__(self):
        self.word_dict = dict()
        self.concept_dict = dict()

    def __iter__(self):
        return iter(self.word_dict)

    def __getitem__(self, word):
        return self.word_dict[word]

    def keys(self):
        return self.word_dict.keys()

    def add_word(self, word):
        if ("_" not in word.word) & (word.word not in word_dict):
            self.word_dict[word.word] = word

    def generate_concept(self):
        pass

class Word():
    def __init__(self, data, gloss, word_dict):
        self.parse(data, gloss)
        self.concept_list = []

    def __str__(self):
        return "Word: %s, Type: %s, Gloss: %s" % (self.word, self.ss_type, ";".join(self.gloss))

    def parse(self, data, gloss):
        self.ss_type = data[2]
        self.word = data[3]
        self.gloss = gloss

    def add_concept(self, concept):
        self.concept_list.append(concept)

class Concept():
    def __init__(self):
        pass

if __name__ == "__main__":
    word_dict = Word_Dictionary()

    for data_type in WN_DATA_TYPE:
        with open(WN_DIR + "dict/data." + data_type) as f:
            data = f.read().split("\n")[29:]
            
        while(data[-1].strip() == ""):
            data = data[:-1]
        
        for idx in range(len(data)):
            data[idx] = data[idx].strip().split("|")
            data[idx], gloss = data[idx][0].strip().split(" "), data[idx][1].strip().split(";")

            n_synset = int(data[idx][3], 16)
            for synset_idx in range(n_synset):
                if np.random.binomial(1, p_drop) == 0:
                    word = Word(data[idx][:3] + [data[idx][4 + (2 * synset_idx)]] + data[idx][4 + n_synset * 2:], gloss, word_dict)
                    word_dict.add_word(word)

    for word in word_dict:
        print(word_dict[word])
        break
