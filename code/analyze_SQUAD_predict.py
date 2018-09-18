import json
import xlsxwriter

predict = "na_elmo_w_dropout_w_charEmb_head8"
target = "dev-v2.0"

with open("/home/asd36952/unist_squad2.0/train/%s/answer/answer.json" % (predict)) as f:
    predict_data = json.load(f)
with open("../data/SQuAD/%s.json" % (target)) as f:
    target_data = json.load(f)

workbook = xlsxwriter.Workbook("../output/analyze_SQuAD_predict_%s.xlsx" % (predict))
worksheet = workbook.add_worksheet()
worksheet.set_default_row(40)
worksheet.set_column(0, 0, 100)
worksheet.set_column(1, 1, 60)
worksheet.set_column(2, 2, 10)
worksheet.set_column(3, 3, 50)
worksheet.set_column(4, 4, 50)
worksheet.set_column(5, 5, 50)

tag_format = workbook.add_format({'text_wrap':True, 'valign':'top', 'align':'center'})
merge_format = workbook.add_format({'text_wrap':True, 'valign':'top'})
cell_format = workbook.add_format({'text_wrap':True, 'valign':'top'})

worksheet.write(0, 0, "Paragraph", tag_format)
worksheet.write(0, 1, "Question", tag_format)
worksheet.write(0, 2, "Unanswerable", tag_format)
worksheet.write(0, 3, "Prediction", tag_format)
worksheet.write(0, 4, "Answers", tag_format)
worksheet.write(0, 5, "Plausible Answers", tag_format)
worksheet.set_row(0, 20)

cursor = 1
for elem in target_data['data']:
    for p in elem['paragraphs']:
        if len(p['qas']) > 1:
            worksheet.merge_range(cursor, 0, cursor + len(p['qas']) - 1, 0, p['context'], merge_format)
        else:
            worksheet.write(cursor, 0, p['context'], merge_format)
        for idx, qa in enumerate(p['qas']):
            worksheet.write(cursor + idx, 1, qa['question'], cell_format)
            worksheet.write(cursor + idx, 2, str(qa['is_impossible']), cell_format)

            if qa['id'] not in predict_data:
                worksheet.write(cursor + idx, 3, "", cell_format)
            else:
                if predict_data[qa['id']] == []:
                    worksheet.write(cursor + idx, 3, "", cell_format)
                else:
                    worksheet.write(cursor + idx, 3, predict_data[qa['id']], cell_format)

            if qa['is_impossible'] is True:
                answer_list = list(set([answer['text'] for answer in qa['plausible_answers']]))
                worksheet.write(cursor + idx, 4, "", cell_format)
                worksheet.write(cursor + idx, 5, ", ".join(answer_list), cell_format)
            else:
                answer_list = list(set([answer['text'] for answer in qa['answers']]))
                worksheet.write(cursor + idx, 4, ", ".join(answer_list), cell_format)
                worksheet.write(cursor + idx, 5, "", cell_format)
        cursor += len(p['qas'])
workbook.close()



