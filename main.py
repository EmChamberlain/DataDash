import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.form['upload-file']
        data = pd.read_csv(file)
        summary_stats = data.describe()
        ss_dict = summary_stats.to_dict()
        return render_template('data.html', data=data.to_html(), summary_data=summary_stats.to_html())

  
if __name__ == '__main__':
    app.run(debug=True)