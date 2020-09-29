import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        file = request.form['upload-file']
        data = pd.read_csv(file)
        plt.figure()
        
        summary_stats = data.describe()
        ss_dict = summary_stats.to_dict()

        #This is all hard corded ...
        box = data.boxplot(column=["Score", "Age"])
        plt.savefig("static/boxplot1.png")
        scores = data["Score"]
        X = [1,2,3,4,5]
        plt.figure()
        plt.scatter(x=X, y=scores)
        plt.savefig("static/scatter_scores.png")
        print("check")

        return render_template('data.html', data=data.to_html(), summary_data=summary_stats.to_html())

  
if __name__ == '__main__':
    app.run(debug=True)