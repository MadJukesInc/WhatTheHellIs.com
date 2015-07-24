from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from server.extensions import cache

static_results = {}
static_results['thing'] = {
    'name': 'thing',
    'description': 'This is the example result'
}

main = Blueprint('main', __name__)
api_namespace = '/api/v1'

@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')

@main.route(api_namespace+'/query/<search>')
def query(search):
    return static_results[search]
