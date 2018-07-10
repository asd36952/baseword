import json

with open("../data/captions_train2014.json") as f:
    data = json.load(f)

data_dict = {}

for elem in data['annotations']:
    if elem['image_id'] in data_dict:
        data_dict[elem['image_id']].append(elem['caption'])
    else:
        data_dict[elem['image_id']] = [elem['caption']]
