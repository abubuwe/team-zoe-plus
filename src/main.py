import sys
import json
import requests

from tqdm import tqdm
from html_modifier import html_accessibility
from flask import Flask, flash, request, redirect, url_for

from errors import ErrorHandler
from utils import debug_picklify

#TODO: Add your Wave key to top_secrets.py
from top_secrets import WAVE_API_KEY

app = Flask(__name__)
app.debug = True

HTTP_EMPTY_RESPONSE = 200
HTTP_BAD_REQUEST = 400

def is_html(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "html"

@app.route("/", methods=['GET', 'POST'])
def get_html():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file found', file=sys.stderr)
            return "", HTTP_BAD_REQUEST
        file = request.files['file']
        if file.filename == '':
            print('No selected file', file=sys.stderr)
            return "", HTTP_BAD_REQUEST

        if not is_html(file.filename):
            print("Uploaded file is not a HTML file", file=sys.stderr)
            return "", HTTP_BAD_REQUEST
        
        return html_accessibility(file)
    
    return "", HTTP_EMPTY_RESPONSE

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@debug_picklify
def query_accessibility_errors(website: str):
  response = requests.get(
     "https://wave.webaim.org/api/request",
     params = {
        "key": WAVE_API_KEY,
        "url": website,
        "format": "json",
        "reporttype": "3"
     }
  )

  if response.status_code != 200:
     raise RuntimeError(f"Wave failed with code {response}. Full response: {response}")

  return response.json()

def process_analysis(results: dict, error_handler: ErrorHandler):
   print(f"Visual analysis URL: {results['statistics']['waveurl']}")
   print(f"Total element count: {results['statistics']['totalelements']}")

   errors, alerts = results['categories']['error']['items'], results['categories']['alert']['items']

   with tqdm(total = len(errors)) as pbar:
      for error_type, error in errors.items():
         pbar.set_description(f"Patching {error_type}...")
         
         try:
            error_handler.handle_error(error_type, error)
         except RuntimeError:
            # TODO: Remove this!
            pass
         
         pbar.update()
   
   # TODO: Handle alerts!

if __name__ == "__main__":
   url = "https://alphagov.github.io/accessibility-tool-audit/test-cases.html"
   error_handler = ErrorHandler(None)

   process_analysis(query_accessibility_errors(url), error_handler)
   app.run()
