from flask import Flask, render_template, request, jsonify
import pymongo
from pymongo import MongoClient
import openai
import os

# Load OpenAI API key
openai.api_key = "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"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test_main']
# db = client['your_database_name']
collection = db['daos']
# collection = db['your_collection_name']


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    result = get_semantic_search_result(query)

    return jsonify(result)


def get_semantic_search_result(query):
    # Perform semantic search using OpenAI API
    response = openai.Answer.create(
        search_model="davinci-codex",
        model="davinci-codex",
        question=query,
        documents=[doc['text'] for doc in collection.find()],
        examples_context="",
        max_responses=1,
        stop=None,
        log_level="info",
        logprobs=None,
        lls_model=None,
        temperature=0.5,
    )

    # Get the best answer
    best_answer = response['choices'][0]['text'].strip()

    # Find the corresponding document
    document = collection.find_one({"text": best_answer})

    return document


if __name__ == '__main__':
    app.run(debug=True)
