from transformers import pipeline
import pdfminer
from pdfminer.high_level import extract_text
import os
import textract

def summarize(input, n=500):
    input = str(input)
    chunks = ['']
    # Split the input into sentences.
    inp_list = input.split('.')
    count = 0
    # While the list of sentences is not empty.
    while len(inp_list) != 0:
        # We check if the current chunk is less than 500 characters.
        if len(chunks[count]) < 500:
            # If it is we add another sentence to it.
            chunks[count] += inp_list.pop(0) + '.'
        else:
            # Otherwise we start a new sentence and append it to our list of chunks.
            chunks.append(inp_list.pop(0) + '.')
            count += 1
    # Without this conditional we will always have a single period as a chunk and 
    # will get weird results from the models training data.
    if len(chunks[-1]) <= 1:
        chunks.pop()
    # Call the huggingface pipeline for summarization
    summarizer = pipeline('summarization')
    outputs = []
    # For every chunk of sentences inside of our chunk list.
    for chunk in chunks:
        # We create a summary for each of the chunks and then append it to our output array.
        json_output = summarizer(chunk, min_length=5, max_length=50)
        str_output = json_output[0]['summary_text']
        output_array = str_output.split('.')
        outputs.append(output_array)
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
    