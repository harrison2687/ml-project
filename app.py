import os
import pandas as pd
import numpy as np
import pickle
import sklearn
import flask
from flask import Flask, redirect, url_for, request, render_template, session, flash
from functools import wraps

app = Flask(__name__)

# config secret key
app.secret_key = 'capstone123'

def login_req(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in with your username and password.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_req
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid credentials.  Please check your credentials and try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_req
def logout():
    session.pop('logged_in', None)
    flash('Logging out of session.')
    return redirect(url_for('login'))

@app.route('/data')
def dataVisualization():
    return render_template('data.html')

def predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 4)
    model = pickle.load(open('predictor.pkl','rb'))
    result = model.predict(to_predict)
    return result[0]

@app.route('/predict', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = predictor(to_predict_list)
        prediction = str(result)
        return render_template('predict.html',prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)