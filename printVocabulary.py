#!/Users/HankWang/anaconda/envs/py36/bin/python

import sys
import re
from termcolor import colored
from googletrans import Translator
from fpdf import FPDF


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


def printFiletype():
    """ print the prompt asking for the file format
        0 means print to PDF file, 1 means print to txt file
    """
    print("Please input the file format you want as the first argument. \
          \n 0 means PDF.\
          \n 1 means txt.")


def printSource():
    """print the prompt asking for source files
    """
    print("Please type all the markdown files , and seperate those by spaces:")


def getFiletype():
    """get file type as test format, return file type user wants
    :returns: file type
    """
    while True:
        printFiletype()
        filetype = input("File format: ")
        if testFiletype(filetype):
            filetype = int(filetype)
            break
        continue
    return filetype


def testFiletype(filetype):
    """test file type

    :filetype: file type wanted
    :returns: valid (1) or not (0)

    """
    try:
        filetype = int(filetype)
        if filetype != 1 and filetype != 0:
            raise "Invalid number"
    except ValueError:
        print(colored("Please input the correct number", 'red'))
        return 0
    except Exception:
        print(colored("Invalid number. Please select correct one.", 'red'))
        return 0
    return 1


def getFiles():
    """get all the source files and test it
    :returns: file name in list
    """
    printSource()
    files = input("Files: ").split(' ')
    return files


def cleaning(vocabulary, output=None):
    """
        cleaning when file name is wrong
    """
    vocabulary.close()
    if not output:
        output.close()


def print2TXT(word, file, translator):
    """print word and translation into txt file

    :word: English
    :file: txt file
    :translator: translation module

    """
    print(word.lower(), end='', file=output)
    if len(word) < 8:
        print("\t"*2, end='', file=output)
    elif len(word) <= 12:
        print("\t", end='', file=output)
    elif len(word) <= 16:
        print("\t", end='', file=output)
    print("\t" + translator.translate(
                word.lower(),
                dest='zh-cn').text, file=output)


def print2PDF(word, translator, hardVocabulary):
    """print word and translation into PDF file

    :word: english word
    :translator: translation module

    """
    if word.lower() in hardVocabulary:
        pdf.set_text_color(220, 20, 60)
        pdf.cell(200, 18, word.lower())
    else:
        pdf.cell(200, 18, word.lower())

    pdf.cell(0, 18, translator.translate(
            word.lower(), dest='zh-cn').text, ln=1)
    pdf.set_text_color(0, 0, 0)


def readHardVocabulary(file):
    """ read hard vocabulary file and save into a dictionary
        and return the dictionary

    :file: the source file
    :returns: all words in dictionary format

    """
    hardVocabulary = {}
    with open(file, 'r') as vocaFile:
        for line in vocaFile:
            words = line.split()
            if words:
                for word in words:
                    hardVocabulary[word.lower()] = 1
    return hardVocabulary


if len(sys.argv) == 1:
    filetype = getFiletype()
    files = getFiles()
elif len(sys.argv) < 3:
    filetype = 0
    files = sys.argv[1:]
else:
    filetype = sys.argv[1]
    if not testFiletype(filetype):
        filetype = getFiletype()
    else:
        filetype = int(filetype)

    files = sys.argv[2:]

translator = initTranslator()

if filetype == 0:
    pdf = initFPDF()
    hardVocabulary = readHardVocabulary('hardVocabulary.md')
else:
    output = open("vocabulary.txt", "w")

for file in files:
    try:
        vocabulary = open(file, 'r')
    except Exception as e:
        if filetype == 1:
            cleaning(vocabulary, output)
        else:
            cleaning(vocabulary)
        raise e

    for line in vocabulary:
        wordList = re.findall(
            r'\*\*\*\`([a-z]*)\`\*\*\*', line, re.M | re.I)
        if wordList:
            for word in wordList:
                if filetype == 1:
                    print2TXT(word, file, translator)
                else:
                    print2PDF(word, translator, hardVocabulary)
    vocabulary.close()

if filetype == 1:
    output.close()
else:
    pdf.output('vocabulary.pdf', 'F').encode('utf-8')
