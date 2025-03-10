# -*- coding: cp1251 -*-
from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# ������������� ��������� ��� ������� ������
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # ������ ������
    result = pipe(text)[0]  # �������� ������ ������� �� ������
    
    # ���������� ������ ��� ������
    sentiment = result['label']
    probability = result['score']
    
    return jsonify({'sentiment': sentiment, 'probability': probability})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)