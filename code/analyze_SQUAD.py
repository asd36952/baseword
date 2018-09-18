import json
import xlsxwriter

target = "train-v2.0_sentence_small"

with open("../data/SQuAD/%s.json" % (target)) as f:
    data = json.load(f)

workbook = xlsxwriter.Workbook("../output/analyze_SQuAD_%s.xlsx" % (target))
worksheet = workbook.add_worksheet()
worksheet.set_default_row(40)
worksheet.set_column(0, 0, 100)
worksheet.set_column(1, 1, 60)
worksheet.set_column(2, 2, 50)

tag_format = workbook.add_format({'text_wrap':True, 'valign':'top', 'align':'center'})
merge_format = workbook.add_format({'text_wrap':True, 'valign':'top'})
cell_format = workbook.add_format({'text_wrap':True, 'valign':'top'})

worksheet.write(0, 0, "Paragraph", tag_format)
worksheet.write(0, 1, "Question", tag_format)
worksheet.write(0, 2, "Answers", tag_format)
worksheet.set_row(0, 20)

cursor = 1
for elem in data['data']:
    for p in elem['paragraphs']:
        if len(p['qas']) > 1:
            worksheet.merge_range(cursor, 0, cursor + len(p['qas']) - 1, 0, p['context'], merge_format)
        else:
            worksheet.write(cursor, 0, p['context'], merge_format)
        for idx, qa in enumerate(p['qas']):
            answer_list = list(set([answer['text'] for answer in qa['answers']]))
            worksheet.write(cursor + idx, 1, qa['question'], cell_format)
            if answer_list == []:
                worksheet.write(cursor + idx, 2, "UNANSWERABLE", cell_format)
            else:
                worksheet.write(cursor + idx, 2, ", ".join(answer_list), cell_format)
        cursor += len(p['qas'])
workbook.close()



