import os
from flask import Flask, render_template, request, g, url_for, flash, session, redirect, Response, session
from datetime import datetime, timedelta
import pytz
import yaml


app = Flask(__name__)
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
app.secret_key = SECRET_KEY


# Для футера
current_year = datetime.now()
current_year = datetime.strftime(current_year, '%Y')

# Для времени
ALA = pytz.timezone('Asia/Almaty')

with open('dictionary.yml', "r", encoding='utf-8') as cnt:
    dictionary = yaml.safe_load(cnt)


@app.route('/set_lang', methods=['POST'])
def set_lang():
    if request.method == 'POST':
        chosen_lang = request.form['language']
        session['interface_language_voice'] = chosen_lang
        url = request.form['url']
        url = url.split('/')[-1]
        if len(url) == 0:
            url = 'index'
        return redirect(url_for(f'{url}'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if not session.get('interface_language_voice'):
        session['interface_language_voice'] = 'en'
    interface_language = session.get('interface_language_voice', None)
    # interface_language = 'ру'
    print(interface_language)
    language_dictionary = dictionary[f'{interface_language}']
    if request.method == 'GET':
        return render_template('index.html', current_year=current_year, language_dictionary=language_dictionary)
    if request.method == 'POST':
        return render_template('index.html', current_year=current_year, language_dictionary=language_dictionary)


@app.route("/login", methods=["POST", "GET"])
def login():
    if not session.get('interface_language_voice'):
        session['interface_language_voice'] = 'en'
    interface_language = session.get('interface_language_voice', None)
    language_dictionary = dictionary[f'{interface_language}']
    if request.method == "GET":
        return render_template("login.html", title="Authorization", current_year=current_year,
                               language_dictionary=language_dictionary)
    if request.method == "POST":
        return render_template("login.html", title="Authorization", current_year=current_year,
                               language_dictionary=language_dictionary)


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT', 5010))
    app.run(debug=True)
