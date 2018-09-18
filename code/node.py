import numpy as np

WN_DIR = "../WordNet-3.0/"
#WN_DATA_TYPE = ["verb", "noun", "adv", "adj"]
WN_DATA_TYPE = ["verb", "adv", "adj"]

p_drop = 0

class Concept():
    def __init__(self):
        pass

class Stem():
    def __init__(self):
        pass

class Stem_Dictionary():
    def __init__(self):
        self.concept_dict = dict()
        self.stem_dict = dict()

    def __iter__(self):
        return iter(self.stem_dict)

    def __setitem__(self, key, value):
        self.stem_dict[key] = value

    def __getitem__(self, stem):
        return self.stem_dict[stem]

    def keys(self):
        return sorted(self.stem_dict.keys(), key=lambda x:len(x))

    def add_stem(self, stem):
        pass

    def generate_concept(self):
        pass

class Word_Dictionary():
    def __init__(self, stem_dict):
        self.stem_dict = stem_dict
        self.word_dict = dict()

    def __iter__(self):
        return iter(self.word_dict)

    def __setitem__(self, key, value):
        self.word_dict[key] = value

    def __getitem__(self, word):
        return self.word_dict[word]

    def keys(self):
        return sorted(self.word_dict.keys(), key=lambda x:len(x))

    def add_word(self, word):
        if ("_" not in word.word):
            if (word.word not in word_dict):
                self.word_dict[word.word] = []

    def stemmize_word(self, word):
        for i in range(len(word)):
            if word[:(i + 1)] in stem_dict:
                if word[(i + 1):] not in stem_dict[word[:(i + 1)]]:
                    stem_dict[word[:(i + 1)]].append(word[(i + 1):])
            else:
                stem_dict[word[:(i + 1)]] = [word[(i + 1):]]

class Word():
    def __init__(self, data, gloss, word_dict):
        self.parse(data, gloss)

    def __str__(self):
        return "Word: %s, Type: %s, Gloss: %s" % (self.word, self.ss_type, ";".join(self.gloss))

    def parse(self, data, gloss):
        self.ss_type = data[2]
        self.word = data[3]
        self.gloss = gloss

if __name__ == "__main__":
    stem_dict = Stem_Dictionary()
    word_dict = Word_Dictionary(stem_dict=stem_dict)

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
        word_dict.stemmize_word(word)
        print(word)
        print()
        for stem in stem_dict.keys():
            print(stem)
            print(stem_dict[stem])
        break
