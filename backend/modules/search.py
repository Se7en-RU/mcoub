from flask import Flask, Blueprint, request, make_response, jsonify
from modules.check import Check
from modules.audio import Audio

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['POST'])
async def search():
  content = request.get_json()

 # No url in POST request provided
  if 'url' not in content:
    return make_response(jsonify({'data': None, 'error': 'No url provided'}), 400)

  checker = Check()
  coub_id = checker.url(content['url'])

  # Cannot parse coub.com url
  if not coub_id:
    return make_response(jsonify({'data': None, 'error': 'Wrong url'}), 400)
  
  # Get data from coub.com
  coub_data = checker.coub_data(coub_id)
  if not coub_data:
    return make_response(jsonify({'data': None, 'error': 'Cannot get data from coub.com'}), 404)

  db_data = checker.coub_exists(coub_id)
  # If coub already in our database - just return it
  if db_data:
    return make_response(jsonify({'data': {'shazam': db_data[0], 'coub': coub_data}, 'error': None}), 200)  
  
  try:
    audio = Audio()
    shazam_data = await audio.search(coub_id, coub_data)
  except Exception as e:
      shazam_data = None
  
  return make_response(jsonify({'data': {'shazam': shazam_data, 'coub': coub_data}, 'error': None}), 200)