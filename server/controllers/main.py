from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required

from server.extensions import cache
from server.frequency import get_frequencies
from server.frequency import get_noun_frequencies

static_results = {}
static_results['thing'] = u'This is the example result'
static_results['kyle'] =  u'The Efficiency Nazi'
static_results['nikita'] = u'The Git Nazi'
static_results['jason'] = u'The Organization Nazi'
static_results['dave'] = u'The Grammar Nazi'

main = Blueprint('main', __name__)
api_namespace = '/api/v1'



@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')

@main.route(api_namespace+'/query/<search>')
def query(search):
    print search
    return  jsonify(query = search , description = static_results[search])

@main.route(api_namespace+'/counts/<search>')
def w_counts(search):
    return jsonify(
    query = search ,
    description = static_results[search],
    counts=get_noun_frequencies(static_results[search]))

@main.route(api_namespace+'/np_counts/<search>')
def np_counts(search):
    return jsonify(
    query = search ,
    description = static_results[search],
    counts=get_frequencies(static_results[search]))
