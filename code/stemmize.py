import numpy as np
import csv

DATA_PATH = "../data/word_frequency/unigram_freq.csv"

vocab_size = 10000

class Concept():
    def __init__(self):
        pass

class Stem():
    def __init__(self, stem):
        self.stem = stem

class Prefix():
    def __init__(self, prefix):
        self.prefix = prefix

class Surffix():
    def __init__(self, surffix):
        self.surffix = surffix

class Stem_Dictionary():
    def __init__(self):
        self.concept_dict = dict()
        self.stem_dict = dict()
        self.prefix_dict = dict()
        self.surffix_dict = dict()

    def __iter__(self):
        return iter(self.stem_dict)

    def __setitem__(self, key, value):
        self.stem_dict[key] = value

    def __getitem__(self, stem):
        return self.stem_dict[stem]

    def keys(self):
        return sorted(self.stem_dict.keys(), key=lambda x:(len(x), x))

    def add_stem(self, stem):
        self.stem_dict[stem] = Stem(stem)

    def add_prefix(self, prefix):
        self.prefix_dict[prefix] = Prefix(prefix)

    def add_surffix(self, surffix):
        self.surffix_dict[surffix] = Surffix(surffix)

    def generate_concept(self):
        pass

class Word_Dictionary():
    def __init__(self):
        self.stem_dict = Stem_Dictionary()
        self.word_dict = dict()
        self.prob_dict = dict()

    def __iter__(self):
        return iter(self.word_dict)

    def __setitem__(self, key, value):
        self.word_dict[key] = value

    def __getitem__(self, word):
        return self.word_dict[word]

    def keys(self):
        return sorted(self.word_dict.keys(), key=lambda x:(len(x), x))

    def add_word(self, word):
        if ("_" not in word.word) & ("-" not in word.word) & ("~" not in word.word):
            if (word.word not in word_dict):
                self.word_dict[word.word] = word

    def compute_prob(self, front_part, back_part):
        if (front_part not in self.prob_dict):
            if (front_part in self.stem_dict):
                self.prob_dict[front_part] = 1.0
            else:
                self.prob_dict[front_part] = 0.0
                for stem in self.stem_dict:
                    if (stem.startswith(front_part) | stem.endswith(front_part)):
                        if (self.prob_dict[front_part] < (len(front_part) / len(stem))):
                            self.prob_dict[front_part] = len(front_part) / len(stem)
                            self.stem_dict[front_part] = self.stem_dict[stem]

        if ((front_part + "-") not in self.prob_dict):
            total = 0
            n_match = 0
            for word in self.word_dict:
                if word.startswith(front_part):
                    total += 1
                    if (word[len(front_part):] in self.word_dict):
                        n_match += 1
            self.prob_dict[front_part + "-"] = n_match / total
         
        if (back_part not in self.prob_dict):
            if (back_part in self.stem_dict):
                self.prob_dict[back_part] = 1.0
            else:
                self.prob_dict[back_part] = 0.0
                for stem in self.stem_dict:
                    if (stem.startswith(back_part) | stem.endswith(back_part)):
                        if (self.prob_dict[back_part] < (len(back_part) / len(stem))):
                            self.prob_dict[back_part] = len(back_part) / len(stem)
                            self.stem_dict[back_part] = self.stem_dict[stem]

        if (("-" + back_part) not in self.prob_dict):
            total = 0
            n_match = 0
            for word in self.word_dict:
                if word.endswith(back_part):
                    total += 1
                    if (word[:-len(back_part)] in self.word_dict):
                        n_match += 1
            self.prob_dict["-" + back_part] = n_match / total
        
        return

    def stemmize(self):
        for word in self.word_dict.keys():
            self.stemmize_word(word)

    def stemmize_word(self, word):
        stem_list = []

        if len(word) == 1:
            stem_list.append([[word], 1.0])
            return stem_list

        total_prob = 0.0

        for i in range(len(word) - 1):
            front_part = word[:(i + 1)]
            back_part = word[(i + 1):]
            self.compute_prob(front_part, back_part)
            """
            if (front_part in self.stem_dict) & (surffix is self.stem_dict):
                stem_list.append([[prefix, surffix], self.prob_dict[prefix] * self.prob_dict[surffix]])
                total_prob += self.prob_dict[prefix] * self.prob_dict[surffix]
            else:
                if (prefix in self.word_dict):
                    stem_list.append([[prefix, "-" + surffix], self.prob_dict[surffix]])
                    total_prob += self.prob_dict[surffix]

                if (surffix in self.word_dict):
                    stem_list.append([[prefix + "-", surffix], self.prob_dict[prefix]])
                    total_prob += self.prob_dict[prefix]
            """
            if (front_part in self.stem_dict):
                stem_list.append([[front_part], [front_part, "-" + back_part], 0.5 * self.prob_dict["-" + back_part]])
                total_prob += 0.5 * self.prob_dict["-" + back_part]

            if (back_part in self.stem_dict):
                stem_list.append([[back_part], [front_part + "-", back_part], 0.5 * self.prob_dict[front_part + "-"]])
                total_prob += 0.5 * self.prob_dict[front_part + "-"]

        stem_list.append([[word], [word], 1.0 - total_prob])
        
        stem_list = list(reversed(sorted(stem_list, key=lambda x:x[2])))
        for stem in stem_list[0][0]:
            if stem not in self.stem_dict:
                self.stem_dict[stem] = Stem(stem)

        return stem_list

class Word():
    def __init__(self, word):
        self.word = word
        self.stem = word
        self.stem_list = [word]

    def __str__(self):
        return "Word: %s\nStem: %s\nStemmization result: " % (self.word, self.stem, " + ".join(self.stem_list))

if __name__ == "__main__":
    word_dict = Word_Dictionary()
    with open(DATA_PATH) as f:
        data = f.read().split("\n")[1:vocab_size]
        
    while(data[-1].strip() == ""):
        data = data[:-1]
    
    for word_freq in data:
        word = Word(word_freq.split(",")[0])
        word_dict.add_word(word)

    word_dict.stemmize()
    for word in word_dict:
        print(word)
        for [stem, result, prob] in word_dict.stemmize_word(word):
            print(" & ".join(stem))
            print(" + ".join(result))
            print(prob)
        input()
