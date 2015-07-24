from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import requests
import operator

from flask.ext.cors import cross_origin
from server.extensions import cache
from server.frequency import get_frequencies
from server.frequency import get_noun_frequencies

static_results = {}
static_results['thing'] = u'This is the example result'
static_results['kyle'] = u'The Efficiency Nazi'
static_results['nikita'] = u'The Git Nazi'
static_results['jason'] = u'The Organization Nazi'
static_results['dave'] = u'The Grammar Nazi'

main = Blueprint('main', __name__)
api_namespace = '/api/v1'
SENTENCES_COUNT = 3
LANGUAGE = "english"

@main.route('/')
@cache.cached(timeout=1000)
def home():
  return render_template('index.html')


@main.route(api_namespace + '/query/<search>')
def query(search):
  print search
  return jsonify(query=search, description=static_results[search])


@main.route(api_namespace + '/counts/<search>')
def w_counts(search):
  return jsonify(
      query=search,
      description=static_results[search],
      counts=get_noun_frequencies(static_results[search]))


@main.route(api_namespace + '/np_counts/<search>')
def np_counts(search):
  return jsonify(
      query=search,
      description=static_results[search],
      counts=get_frequencies(static_results[search]))

wiki_request_uri = 'https://en.wikipedia.org/w/api.php?' \
    'format=json&'\
    'action=query&'\
    'prop=extracts&'\
    'exintro=&'\
    'explaintext=&'\
    'titles='

def perform_request(search):
    data = requests.get(wiki_request_uri + search).json()
    content = ''
    urls = ''
    pages = data['query']['pages']
    for pageID in pages:
        query = pages[pageID]
        content = query['extract']
        urls = 'https://en.wikipedia.org/?curid=' + str(query['pageid'])
        return {'content':content, 'url': urls}

def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    result = ''
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        result += str(sentence)
    return result

# def sortNSplit(unsorted):
#     return sorted(unsorted)

@main.route(api_namespace + '/wiki/<search>')
@cross_origin()
def wiki(search):
  result = perform_request(search)
  return jsonify(result)


@main.route(api_namespace + '/wiki/<search>/wc')
@cross_origin()
def wiki_wc(search):
  result = perform_request(search)
  print result

  urls = result['url']
  summaries = summarize(result['content'])
  counts = get_noun_frequencies(result['content'])

  return jsonify(counts=counts,summaries=summaries,urls=urls)
