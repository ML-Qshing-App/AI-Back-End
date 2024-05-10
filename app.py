import joblib
import pandas as pd
from urllib.parse import urlparse, parse_qs
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Union

model = joblib.load("model.pkl")

def extract_features(url):
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    hostname = parsed_url.hostname if parsed_url.hostname else 'None'
    path = parsed_url.path
    params = parsed_url.params
    query_params = ';'.join(['{}={}'.format(k, ','.join(v)) for k, v in parse_qs(parsed_url.query).items()])
    fragment = parsed_url.fragment

    special_chars = "!@#$%^&*()-_+=[]{}|;:,.<>/?"
    special_char_counts = [url.count(char) for char in special_chars]

    url_length = len(url)
    url_bytes = len(url.encode('utf-8'))

    return [protocol, hostname, path, params, query_params, fragment] + special_char_counts + [url_length, url_bytes]

def extract_features_2(data):
    if isinstance(data, str):
        data = [data]
    parsed_data = []
    special_chars = "!@#$%^&*()-_+=[]{}|;:,.<>/?"
    special_char_columns = [f'Special_Char_{char}' for char in special_chars]
    columns = ['Protocol', 'Hostname', 'Path', 'Params', 'Query_Params', 'Fragment'] + special_char_columns + ['URL_Length', 'URL_Bytes']

    for url in data:
        parsed_data.append(extract_features(url))

    df_parsed_data = pd.DataFrame(parsed_data, columns=columns)
    df_parsed_data = df_parsed_data.dropna(axis=1)
    return df_parsed_data

app = Flask(__name__)
CORS(app)

@app.route("/url_ai/", methods=["GET"])
def predict():
    data = request.args.get('data')
    if not data:
        return jsonify({"error": "No URL provided"}), 400

    processing_data = extract_features_2(data=data)
    prediction = int(model.predict(processing_data)[0])

    return jsonify({"result": prediction})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
