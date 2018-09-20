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
        return sorted(self.stem_dict.keys(), key=lambda x:(len(x), x))

    def add_stem(self, stem):
        pass

    def generate_concept(self):
        pass

class Word_Parser():
    def __init__(self):
        prob_dict = dict()

    def parse(self, word):
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
                self.word_dict[word.word] = []

    def compute_prob(self, prefix, surffix):
        if prefix not in self.prob_dict:
            total = 0
            n_match = 0
            for word in self.word_dict:
                if word.startswith(prefix):
                    total += 1
                    if word[len(prefix):] in self.word_dict:
                        n_match += 1
            if total > 1:
                self.prob_dict[prefix] = n_match / total
            else:
                self.prob_dict[prefix] = 0.0
         
        if surffix not in self.prob_dict:
            total = 0
            n_match = 0
            for word in self.word_dict:
                if word.endswith(surffix):
                    total += 1
                    if word[:-len(surffix)] in self.word_dict:
                        n_match += 1
            if total > 1:
                self.prob_dict[surffix] = n_match / total
            else:
                self.prob_dict[surffix] = 0.0
        
        return

    def stemmize_word(self, word):
        stem_list = []

        if len(word) == 1:
            stem_list.append([[word], 1.0])
            return stem_list

        total_prob = 0.0

        for i in range(len(word) - 1):
            prefix = word[:(i + 1)]
            surffix = word[(i + 1):]
            self.compute_prob(prefix, surffix)

            if (prefix in self.word_dict) & (surffix is self.word_dict):
                stem_list.append([[prefix, surffix], self.prob_dict[prefix] * self.prob_dict[surffix]])
                total_prob += self.prob_dict[prefix] * self.prob_dict[surffix]
            else:
                if (prefix in self.word_dict):
                    stem_list.append([[prefix, "-" + surffix], self.prob_dict[surffix]])
                    total_prob += self.prob_dict[surffix]

                if (surffix in self.word_dict):
                    stem_list.append([[prefix + "-", surffix], self.prob_dict[prefix]])
                    total_prob += self.prob_dict[prefix]
        stem_list.append([[word], 1.0 - total_prob])
        return reversed(sorted(stem_list, key=lambda x:x[1]))

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
        print(word)
        for [stem, prob] in word_dict.stemmize_word(word):
            print("\t".join(stem))
            print(prob)
        input()
