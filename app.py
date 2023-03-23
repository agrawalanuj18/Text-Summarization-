import nltk
from flask import Flask, render_template, request
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest


app = Flask(__name__)

def summarize():
    text = request.form['text']
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_frequencies = FreqDist(filtered_words)
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]
    summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    print(summary)
    return summary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def summarize_text():
    summary = summarize()
    text = request.form['text']
    return render_template('summary.html', summary=summary, text=text)

if __name__ == '__main__':
    app.run(debug=True)