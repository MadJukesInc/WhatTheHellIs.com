from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user, login_required

from server.extensions import cache

static_results = {}
static_results['thing'] = u'This is the example result'
static_results['kyle'] =  u'The Efficiency Nazi'
static_results['nikita'] = u'The Git Nazi'
static_results['jason'] = u'The Organization Nazi'

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
