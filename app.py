from flask import Flask, request, make_response, jsonify
from coub import Coub

app = Flask(__name__)

@app.route('/search', methods=['POST'])
async def search():
  url = request.form.get('url')

  if not url:
    return make_response(jsonify({'error': 'No url provided'}), 400)

  coub = Coub()
  data = await coub.search(url)

  if not data or 'track' not in data:
    return make_response(jsonify({'data': None}), 200)

  return make_response(jsonify({'data': data}), 200)