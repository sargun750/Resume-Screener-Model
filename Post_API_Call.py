from flask import Flask, request, jsonify
import requests
import fitz  # Module from PyMuPDF library
import os
import json
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer, util

from PDF_Conversion import pdf_to_text
from LLM_api import mistral_7b_score
from S_BERT_Model import sentence_bert

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/findscore', methods=['POST'])
def register_user():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    # Check if text was provided
    if 'text' not in request.form:
        return jsonify({'error': 'No text string provided'}), 400
    
    file = request.files['pdf']
    Job_desc = request.form['text']
    # Validate PDF file
    if file.filename == '':
        return jsonify({'error': 'No selected PDF file'}), 400
    
    if file and allowed_file(file.filename):
        # Save the file temporarily

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        Resume_text = pdf_to_text(filepath)

        LLM_response = mistral_7b_score(Resume_text, Job_desc)
        LLM_Score = int(LLM_response["score"])
        Reason = LLM_response['reason']

        Score = sentence_bert(Resume_text, Job_desc)
        SBERT_Score = round(Score * 100, 2)

        Final = 0.25 * SBERT_Score + 0.75 * LLM_Score # Coeff can be adjusted
        return jsonify({'Sentence BERT Score':SBERT_Score,
                       'LLM Model Score':LLM_Score},
                       {'COMPATIBILITY SCORE':Final},
                       {'REASONS':Reason}), 200

    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
