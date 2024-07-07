from flask import Flask, request, jsonify, send_from_directory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory(os.getcwd(), 'style.css')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    feedback = data['feedback']
    sentiment_score = analyzer.polarity_scores(feedback)
    if sentiment_score['compound'] >= 0.05:
        result = 'Positive 😊'
    elif sentiment_score['compound'] <= -0.05:
        result = 'Negative 😞'
    else:
        result = 'Neutral 🤗'
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)