# https://stackoverflow.com/a/59939341 -- ref
# https://stackoverflow.com/a/63652502 -- ref 2
import os
import requests
import logging
import re
from flask import (Flask, render_template, request, redirect, session, jsonify)
from werkzeug.wrappers import response

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
app = Flask(__name__)
app.secret_key = 'ItShouldBeAnythingButSecret'

user = {"username": "abc", "password": "xyz"}


@app.route('/')
def hello():
    return 'Hello'


steam64_from_url = "^https:\/\/steamcommunity\.com\/openid\/id\/(\d+)$"


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route('/steam_login', methods=['GET'])
def openid_login():
    good_response = request.args.get('openid.mode') == 'id_res'

    # current problem - cannot read from localhost
    print(request.headers.get('User-Agent'))

    if good_response:
        required = [
            'openid.ns',
            'openid.mode',
            'openid.op_endpoint',
            'openid.claimed_id',
            'openid.identity',
            'openid.return_to',
            'openid.assoc_handle',
            'openid.op_endpoint',
            'openid.sig',
            'openid.signed',
            'openid.response_nonce'
        ]
        params = {
            item: request.args.get(item)
            for item in required
        }
        response = requests.get(
            'https://steamcommunity.com/openid/login', params=params)

        if response.text.find('is_valid:true'):
            steam64 = re.match(
                steam64_from_url,
                params['openid.claimed_id']
            ).group(1)
            session['steam64'] = steam64
            return redirect('/dashboard')
        else:
            return "Invalid login"

    return 'nah'


@ app.route('/logout')
def logout():
    session.pop('steam64')
    return redirect('/login')


@ app.route('/dashboard')
def dashboard():
    if 'steam64' in session:
        return '<h1>Welcome to the dashboard</h1>'

    return '<h1>You are not logged in.</h1>'  # if the user is not in the session


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
