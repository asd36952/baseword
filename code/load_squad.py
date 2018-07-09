import json

with open("../data/train-v2.0.json") as f:
    data = json.load(f)

data_dict = {}

for elem in data['data']:
    data_dict[elem['title']] = []
    for p in elem['paragraphs']:
        for qa in p['qas']:
            print(p['context'])
            print(qa['question'])
            print(qa['answers'])
            input()



