from flask import Flask, request, make_response, jsonify
from check import Check
from audio import Audio

app = Flask(__name__)

@app.route('/search', methods=['POST'])
async def search():
  url = request.form.get('url')

  checker = Check()
  coub_id = checker.url(url)

  # No url in POST request provided
  if not url:
    return make_response(jsonify({'data': None, 'error': 'No url provided'}), 400)

  # Cannot parse coub.com url
  if not coub_id:
    return make_response(jsonify({'data': None, 'error': 'Wrong url'}), 400)
  
  # Get data from coub.com
  coub_data = checker.coub_data(coub_id)
  if not coub_data:
    return make_response(jsonify({'data': None, 'error': 'Cannot get data from coub.com'}), 500)

  db_data = checker.coub_exists(coub_id)
  # If coub already in our database - just return it
  if db_data:
    return make_response(jsonify({'data': {'shazam': db_data, 'coub': coub_data}, 'error': None}), 200)  
  
  try:
    audio = Audio()
    shazam_data = await audio.search(coub_id, coub_data)
  except Exception as e:
    return make_response(jsonify({'data': None, 'error': str(e)}), 500)
  
  return make_response(jsonify({'data': {'shazam': shazam_data, 'coub': coub_data}, 'error': None}), 200)