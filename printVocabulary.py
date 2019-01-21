#!/Users/HankWang/anaconda/envs/py36/bin/python

import sys
import re
from googletrans import Translator
from fpdf import FPDF


"""
0 means print to PDF file, 1 means print to txt file
"""
try:
    filetype = int(sys.argv[1])
    if filetype != 1 and filetype != 2:
        raise "Invalid number"
except Exception as e:
    print("Please input the file format you want as the first argument. \
          \n 0 means PDF.\
          \n 1 means txt.")
    raise e


def initFPDF():
    pdf = FPDF('P', 'pt', 'A4')
    pdf.add_page()
    pdf.add_font(
        'Custom',
        '',
        '/Users/HankWang/Documents/Fonts/ARIALUNI.TTF',
        uni=True)

    pdf.set_font('Custom', '', 16)
    return pdf


def initTranslator():
    translator = Translator()
    return translator


printFormat = int(sys.argv[1])
pdf = initFPDF()
translator = initTranslator()


if printFormat == 1:
    output = open("vocabulary.txt", "w")

for file in sys.argv[2:]:
    with open(file)as vocabulary:
        for line in vocabulary:
            wordList = re.findall(
                r'\*\*\*\`([a-z]*)\`\*\*\*', line, re.M | re.I)
            if wordList:
                for word in wordList:
                    if printFormat == 1:
                        print(word.lower(), end='', file=output)
                        if len(word) < 8:
                            print("\t"*2, end='', file=output)
                        elif len(word) <= 12:
                            print("\t", end='', file=output)
                        print("\t" +
                              translator.translate(
                                    word.lower(),
                                    dest='zh-cn').text, file=output)
                    else:
                        pdf.cell(200, 18, word.lower())
                        pdf.cell(
                            0, 18, translator.translate(
                                word.lower(), dest='zh-cn').text, ln=1)

if printFormat == 1:
    output.close()
else:
    pdf.output('vocabulary.pdf', 'F').encode('utf-8')
