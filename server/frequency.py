from textblob import TextBlob

def get_frequencies(text):
    blob = textblob(text)
    return blob.np_counts
