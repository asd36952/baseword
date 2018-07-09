import json

with open("../data/train-v2.0.json") as f:
    data = json.load(f)

para_list = []

for i in range(len(data['data'])):
    for j in range(len(data['data'][i]['paragraphs'])):
        para_list.append(data['data'][i]['paragraphs'][j]['context'])

para_list = sorted(para_list, key = len)

for elem in para_list:
    print(elem)
    print(len(elem))
    input()
