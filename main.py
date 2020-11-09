import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import matplotlib.pyplot as plt
import math
import pathlib

UPLOAD_FOLDER = '/tmp'



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# randomly generated with print(os.urandom(24))
app.secret_key = b'&\xa1\x89\xb8\xdd\x07\xad\xfd\xa3/\xe8\x03\x18\x06XK\xef\x87\xfekn\xd6n\xa5'




Min = 0
Q1 = 0
Median = 0
Q2 = 0
Max = 0
Mean = 0
df = pd.DataFrame()
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        if len(request.files) == 0:
            flash("No file part")
            return redirect(request.url)
        global df
        f = request.form['upload-file']
        path = pathlib.Path(__file__).parent.absolute()
        print("PATH " + str(path))
        file = os.path.join(path, f)
        df = pd.read_csv(file)
        plt.figure()
        print(df)
        summary_stats = df.describe()
        ss_dict = summary_stats.to_dict()

        box = df.boxplot(column=["Score"])
        plt.savefig(os.path.join(path, "static/boxplot.png"))

        plt.figure()
        df['Score'].value_counts().plot('bar')
        plt.savefig(os.path.join(path, "static/frequency1.png"))

        plt.figure()
        df.hist(bins=10)
        plt.savefig(os.path.join(path, "static/histogram.png"))

        global Min
        global Q1
        global Median
        global Q2
        global Max
        global Mean

        Min = ss_dict['Score']['min']
        Q1 = ss_dict['Score']['25%']
        Median = ss_dict['Score']['50%']
        Q2 = ss_dict['Score']['75%']
        Max = ss_dict['Score']['max']
        Mean = ss_dict['Score']['mean']
        # inject_dict_for_all_templates(ss_dict)
        return render_template('data.html', data=df.to_html(), summary_data=summary_stats.to_html(),
                           mean=round(ss_dict['Score']['mean'], 2), count=round(ss_dict['Score']['count']), std=round(ss_dict['Score']['std'], 2),
                           lower=round(
                               ss_dict['Score']['mean'] - ss_dict['Score']['std'], 2),
                           min=ss_dict['Score']['min'], q1=ss_dict['Score']['25%'], q2=ss_dict['Score']['50%'],
                           q3=ss_dict['Score']['75%'], max=ss_dict['Score']['max'])
    else:
        flash("No file part")
        return redirect(url_for('index'))


@app.route('/boxplot', methods=['GET', 'POST'])
def boxplot():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
    # print("HEREEEEEEE")
    # print(Mean)
    # show the form, it wasn't submitted
    global Min
    global Q1
    global Median
    global Q2
    global Max

    return render_template('boxplot.html', min=Min, max=Max, q1=Q1, q2=Median, q3=Q2)


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('histogram.html')


@app.route('/frequency', methods=['GET', 'POST'])
def frequency():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('frequency.html')


@app.route('/flatscale', methods=['GET', 'POST'])
def flatscale():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted

    df["Score"] += (100-Max)
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig("static/boxplotfs.png")

    plt.figure()
    df['Score'].value_counts().plot('bar')
    plt.savefig("static/frequencyfs.png")

    plt.figure()
    df.hist(bins=10)
    plt.savefig("static/histogramfs.png")
    return render_template('flatscale.html', data=df.to_html(), summary_data=summary_stats.to_html())


@app.route('/linearscale', methods=['GET', 'POST'])
def linearscale():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted

    df_copy = df

    summary_stats = df_copy.describe()
    ss_dict = summary_stats.to_dict()
    a = ((Max + 2) - (Min + 8)) / (Max - Min)
    for index, row in df_copy.iterrows():
        df_copy.at[index, "Score"] = 85 + a*(row["Score"] - Mean)

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig("static/boxplotls.png")

    plt.figure()
    df['Score'].value_counts().plot('bar')
    plt.savefig("static/frequencyls.png")

    plt.figure()
    df.hist(bins=10)
    plt.savefig("static/histogramls.png")
    return render_template('linearscale.html', data=df_copy.to_html(), summary_data=summary_stats.to_html())


@app.route('/rootscale', methods=['GET', 'POST'])
def rootscale():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    df_copy = df

    summary_stats = df_copy.describe()
    ss_dict = summary_stats.to_dict()
    for index, row in df_copy.iterrows():
        df_copy.at[index, "Score"] = 10 * math.sqrt(row["Score"])

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig("static/boxplotrs.png")

    plt.figure()
    df['Score'].value_counts().plot('bar')
    plt.savefig("static/frequencyrs.png")

    plt.figure()
    df.hist(bins=10)
    plt.savefig("static/histogramrs.png")
    return render_template('rootscale.html', data=df_copy.to_html(), summary_data=summary_stats.to_html())


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
