import spacy
import json
from stanfordcorenlp import StanfordCoreNLP
import os
import copy

# open StanfordCoreNLP Server by
# java -Djava.io.tmpdir=/home/asd36952/tmp -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9001 -timeout 15000

nlp = StanfordCoreNLP('http://localhost', port=9001)

with open("../data/SQuAD/train-v2.0.json") as f:
    data = json.load(f)

new_data = {'version':'v2.0_sentence_combine', 'data':copy.deepcopy(data['data'])}
#new_data = {'version':'v2.0_sentence', 'data':[]}

for cnt, elem in enumerate(data['data']):
#    if cnt > 3:
#        break
    tmp_data = dict()
    tmp_data['title'] = elem['title']
    tmp_data['paragraphs'] = []

    for p in elem['paragraphs']:

        annotated = nlp.annotate(p['context'], {'annotators':'ssplit', 'outputFormat':'text'})

        sent_list = []
        offset_list = []

        next_flag = False
        new_flag = True
        sent = ""
        for line in annotated.split("\n"):
            #print(line)
            if next_flag is False:
                if (line.startswith("Sentence #")) & (line.endswith("tokens):")): 
                    next_flag = True

                else:
                    offset = line.split(" ")
                    if len(offset) > 2:
                        if new_flag is True:
                            #print(offset)
                            begin_offset = offset[-2]
                            begin_offset = int(begin_offset[len("CharacterOffsetBegin="):])
                            new_flag = False
                        else:
                            end_offset = offset[-1]
                            end_offset = int(end_offset[len("CharacterOffsetEnd="):-1])

            else:
                if len(sent_list) > len(offset_list):
                    offset_list.append([begin_offset, end_offset])

                sent += line
                if line == "":
                    sent_list.append(sent)
                    next_flag = False
                    new_flag = True
                    sent = ""

        offset_list.append([begin_offset, end_offset])

        for i in range(len(sent_list)):
            tmp_paragraph = {'context':sent_list[i]}
            tmp_qas = []

            for qa in p['qas']:
                find_candidate = False
                tmp_candidate = []
                if qa['is_impossible'] is True:
                    #if 'plausible_answers' not in qa:
                    #    continue
                    answer_list = qa['plausible_answers']
                else:
                    answer_list = qa['answers']

                for ans in answer_list:
                    if (ans['answer_start'] >= offset_list[i][0]) & (ans['answer_start'] <= offset_list[i][1]):
                        if qa['is_impossible'] is False:
                            if {'text':ans['text'], 'answer_start':(ans['answer_start'] - offset_list[i][0])} not in tmp_candidate:
                                tmp_candidate.append({'text':ans['text'], 'answer_start':(ans['answer_start'] - offset_list[i][0])})
                        find_candidate = True

                if (find_candidate is True):
                    if qa['is_impossible'] is True:
                        tmp_qas.append({'is_impossible':qa['is_impossible'],
                            'answers':[],
                            'plausible_answers':tmp_candidate,
                            'id':qa['id'],
                            'question':qa['question']})
                    else:
                        tmp_qas.append({'is_impossible':qa['is_impossible'],
                            'answers':tmp_candidate,
                            'id':qa['id'],
                            'question':qa['question']})
                
            if tmp_qas != []:
                tmp_paragraph['qas'] = tmp_qas
                tmp_data['paragraphs'].append(tmp_paragraph)

    if tmp_data['paragraphs'] != []:
       new_data['data'].append(tmp_data)

nlp.close()

with open("../data/SQuAD/train-v2.0_sentence_combine.json", "w") as f:
    json.dump(new_data, f)
