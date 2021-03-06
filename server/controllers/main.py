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

main = Blueprint('main', __name__)
api_namespace = '/api/v1'
SENTENCES_COUNT = 3
LANGUAGE = "english"

wiki_request_uri = 'https://en.wikipedia.org/w/api.php?' \
    'format=json&'\
    'action=query&'\
    'prop=extracts&'\
    'exintro=&'\
    'explaintext=&'\
    'titles='


def perform_request(search):
  content = ''
  urls = ''
  try:
    data = requests.get(wiki_request_uri + search).json()
    pages = data['query']['pages']

    for pageID in pages:
      query = pages[pageID]
      try:
        content = query['extract']
        urls = 'https://en.wikipedia.org/?curid=' + str(query['pageid'])
      except KeyError:
        content = 'No data to parse'
        print 'No data in extract'

  except requests.exceptions.Timeout:
    print 'Request Timeout'
  except requests.exceptions.TooManyRedirects:
    print 'Too many redirects'
  except requests.exceptions.RequestException as e:
    print e
  return {'content': content, 'url': urls}


def summarize(text):
  parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
  stemmer = Stemmer(LANGUAGE)
  summarizer = Summarizer(stemmer)
  summarizer.stop_words = get_stop_words(LANGUAGE)
  result = ''

  for sentence in summarizer(parser.document, SENTENCES_COUNT):
    result += str(sentence) + ' '

  return result


@main.route('/')
def home():
  return render_template('index.html')


@main.route(api_namespace + '/query/<search>')
def query(search):
  url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=' + search + '&utf8=&rawcontinue='
  result = requests.get(url).json()
  temp = result['query']['search']
  return jsonify(results=temp)


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
  urls = result['url']
  summaries = summarize(result['content'])
  counts = get_noun_frequencies(result['content'])

  return jsonify(counts=counts, summaries=summaries, urls=urls)
