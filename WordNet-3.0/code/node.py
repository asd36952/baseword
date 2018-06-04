import numpy as np

WN_DIR = "/home/asd36952/WordNet-3.0/"
WN_DATA_TYPE = ["verb", "noun", "adv", "adj"]

p_drop = 0

class Node():
    def __init__(self, data, gloss, p_drop):
        self.parse(data, gloss)

    def __str__(self):
        return "Synset Offset: %d, Word: %s, Type: %s, Definition: %s" % (self.synset_offset, self.word, self.ss_type, self.definition)

    def parse(self, data, gloss):
        self.synset_offset = int(data[0])
        self.ss_type = data[2]
        self.word = data[3] 
        self.definition = gloss[0]

class Base():
    def __init__(self):
        pass

if __name__ == "__main__":
    node_list = []

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
                    node_list.append(Node(data[idx][:3] + [data[idx][4 + (2 * synset_idx)]] + data[idx][4 + n_synset * 2:], gloss, p_drop))

    for idx in range(5):
        print(node_list[-idx])
