import os
import requests

from tqdm import tqdm
from html_modifier import parse_html
from flask import Flask, request

from errors import AccessibilityEditor
from utils import debug_picklify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.debug = True

ACCESSIBILITY_API_URL = "https://alphagov.github.io/accessibility-tool-audit/test-cases.html" 
HTTP_EMPTY_RESPONSE = 200
WAVE_API_KEY = os.getenv("WAVE_API_KEY")

@app.route("/", methods=['GET', 'POST'])
def get_html():
    if request.method == 'POST':
        url = request.args["url"]
        html_string = request.args["html_string"]

        dom = parse_html(html_string)
        accessibility_editor = AccessibilityEditor(dom)
        
        return process_analysis(query_accessibility_errors(ACCESSIBILITY_API_URL), accessibility_editor)
    
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

def process_analysis(results: dict, error_handler: AccessibilityEditor):
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
   app.run()
