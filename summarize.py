from transformers import pipeline
import pdfminer
from pdfminer.high_level import extract_text
import os
import textract
import re

def summarize(input, n=500):
    input = str(input).strip()
    chunks = input.split('\n')
    summarizer = pipeline('summarization')
    outputs = []
    for chunk in chunks:
        if len(chunk) < 10:
            continue
        else:
            json_output = summarizer(chunk, min_length=5, max_length=140)
            str_output = json_output[0]['summary_text'][0:-2] + '.'
            outputs.append(str_output)
    print(outputs)
    return outputs

# Turns our PDF files into text to be broken down.
def pdfToText(file):
    file.save('temp.pdf')
    text = extract_text('temp.pdf', password='', page_numbers=None, maxpages=0, caching=True, codec='utf-8', laparams=None)
    os.remove('temp.pdf')
    return text

def txt_to_text(file):
    file.save('temp.txt')
    with open('temp.txt', 'r') as f:
        text = f.read()
    os.remove('temp.txt')
    return text

def other_to_text(file):
    file.save(file.filename)
    text = textract.process(file.filename)
    os.remove(file.filename)
    return text