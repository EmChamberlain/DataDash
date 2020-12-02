import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, make_response
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import matplotlib.pyplot as plt
import math
import pathlib

uploadPath = os.path.join(os.getcwd(), '\\FileStorage')
cookieMaxAge = 60*60*24*7
cookieID = 'CurrentID'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = uploadPath
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# randomly generated with print(os.urandom(24))
app.secret_key = b'&\xa1\x89\xb8\xdd\x07\xad\xfd\xa3/\xe8\x03\x18\x06XK\xef\x87\xfekn\xd6n\xa5'


@app.route('/images', methods=['GET', 'POST'])
def images():
    return send_from_directory(os.path.join(uploadPath,
                                            secure_filename(request.cookies.get(cookieID))),
                               secure_filename(request.args.get('filename')))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def server_error(e):
    return render_template("public/500.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    # If it is POST request the redirect 
    if request.method =='POST': 
        return redirect(url_for('index'))
    return render_template('index.html')


def randomName():
    return str(os.urandom(10).hex())


def saveNewFile(fileStorageIn):
    extension = os.path.splitext(fileStorageIn.name)[1]
    newName = randomName()
    while os.path.isdir(os.path.join(uploadPath, newName)):
        newName = randomName()

    os.makedirs(os.path.join(uploadPath, newName))

    fileStorageIn.save(os.path.join(uploadPath, newName, 'data.csv'))
    return newName


@app.route('/data', methods=['GET', 'POST'])
def data():
    df = pd.DataFrame()
    if request.method == 'POST':
        if request.files['upload-file'].filename == '':
            return render_template('error.html')

        fileStorObj = request.files['upload-file']
        cookieName = saveNewFile(fileStorObj)
        df = pd.read_csv(os.path.join(uploadPath, cookieName, 'data.csv'))
    else:
        cookieName = request.cookies.get(cookieID)
        df = pd.read_csv(os.path.join(
            uploadPath, request.cookies.get(cookieID), 'data.csv'))

    if "Score" not in df:
        return render_template('error.html')
    plt.figure()
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()

    box = df.boxplot(column=["Score"])
    plt.savefig(os.path.join(uploadPath, cookieName, "boxplot.png"))

    plt.figure()
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    df['Score'].value_counts().sort_index().plot(kind='bar')
    plt.savefig(os.path.join(uploadPath, cookieName, "frequency.png"))

    plt.figure()
    df.hist(bins=10)
    plt.savefig(os.path.join(uploadPath, cookieName, "histogram.png"))

    response = make_response(render_template('data.html', data=df.to_html(), summary_data=summary_stats.to_html(),
                                             mean=round(ss_dict['Score']['mean'], 2), count=round(ss_dict['Score']['count']), std=round(ss_dict['Score']['std'], 2),
                                             lower=round(
        ss_dict['Score']['mean'] - ss_dict['Score']['std'], 2),
        min=ss_dict['Score']['min'], q1=ss_dict['Score']['25%'], q2=ss_dict['Score']['50%'],
        q3=ss_dict['Score']['75%'], max=ss_dict['Score']['max']))
    response.set_cookie(cookieID, cookieName, max_age=cookieMaxAge)
    return response


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

    df = pd.read_csv(os.path.join(
        uploadPath, request.cookies.get(cookieID), 'data.csv'))
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()

    Min = ss_dict['Score']['min']
    Q1 = ss_dict['Score']['25%']
    Median = ss_dict['Score']['50%']
    Q2 = ss_dict['Score']['75%']
    Max = ss_dict['Score']['max']

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

    cookieName = request.cookies.get(cookieID)

    # show the form, it wasn't submitted
    df = pd.read_csv(os.path.join(uploadPath, cookieName, 'data.csv'))
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()

    Max = ss_dict['Score']['max']

    df["Score"] += (100-Max)
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig(os.path.join(uploadPath, cookieName, "boxplotfs.png"))

    plt.figure()
    df['Score'].value_counts().sort_index().plot(kind='bar')
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(uploadPath, cookieName, "frequencyfs.png"))

    plt.figure()
    df.hist(bins=10)
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(uploadPath, cookieName, "histogramfs.png"))
    return render_template('flatscale.html', data=df.to_html(), summary_data=summary_stats.to_html())


@app.route('/linearscale', methods=['GET', 'POST'])
def linearscale():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    cookieName = request.cookies.get(cookieID)

    # show the form, it wasn't submitted
    df = pd.read_csv(os.path.join(uploadPath, cookieName, 'data.csv'))
    summary_stats = df.describe()
    ss_dict = summary_stats.to_dict()
    df_copy = df

    Min = ss_dict['Score']['min']
    Max = ss_dict['Score']['max']
    Mean = ss_dict['Score']['mean']

    summary_stats = df_copy.describe()
    ss_dict = summary_stats.to_dict()
    a = ((Max + 2) - (Min + 8)) / (Max - Min)
    for index, row in df_copy.iterrows():
        df_copy.at[index, "Score"] = 85 + a*(row["Score"] - Mean)

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig(os.path.join(uploadPath, cookieName, "boxplotls.png"))

    plt.figure()
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    df['Score'].value_counts().sort_index().plot(kind='bar')
    plt.savefig(os.path.join(uploadPath, cookieName, "frequencyls.png"))

    plt.figure()
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    df.hist(bins=10)
    plt.savefig(os.path.join(uploadPath, cookieName, "histogramls.png"))

    return render_template('linearscale.html', data=df_copy.to_html(), summary_data=summary_stats.to_html())


@app.route('/rootscale', methods=['GET', 'POST'])
def rootscale():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    cookieName = request.cookies.get(cookieID)

    # show the form, it wasn't submitted
    df = pd.read_csv(os.path.join(uploadPath, cookieName, 'data.csv'))
    df_copy = df

    summary_stats = df_copy.describe()
    ss_dict = summary_stats.to_dict()
    for index, row in df_copy.iterrows():
        df_copy.at[index, "Score"] = 10 * math.sqrt(row["Score"])

    plt.figure()
    box = df.boxplot(column=["Score"])
    plt.savefig(os.path.join(uploadPath, cookieName, "boxplotrs.png"))

    plt.figure()
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    df['Score'].value_counts().sort_index().plot(kind='bar')
    plt.savefig(os.path.join(uploadPath, cookieName, "frequencyrs.png"))

    plt.figure()
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    df.hist(bins=10)
    plt.savefig(os.path.join(uploadPath, cookieName, "histogramrs.png"))
    return render_template('rootscale.html', data=df_copy.to_html(), summary_data=summary_stats.to_html())


@app.after_request
def add_header(r):
    r.cache_control.no_cache = True
    r.cache_control.no_store = True
    r.cache_control.must_revalidate = True
    r.expires = 0
    return r


if __name__ == '__main__':
    app.run(debug=True)
