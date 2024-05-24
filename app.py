from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wordcount', methods=['POST'])
def wordcount():
    text = request.form['text']
    word_count = len(text.split())
    return render_template('result.html', word_count=word_count)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
