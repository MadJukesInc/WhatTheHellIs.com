from textblob import TextBlob

def get_noun_frequencies(text):
    blob = TextBlob(text)
    return blob.np_counts

def get_frequencies(text):
    blob = TextBlob(text)
    return blob.word_counts
