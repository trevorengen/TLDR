from transformers import pipeline

def query_notebook(query, context):
    transformer = pipeline('question-answering')
    result = transformer(query, context)
    # Returns dictionary {'answer': answer, 'score': score, 'start': startloc, 'end': endloc}
    return result