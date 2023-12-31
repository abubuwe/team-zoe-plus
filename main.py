import os
import requests
import os
from itertools import chain

from tqdm import tqdm
from html_modifier import parse_html
from flask import Flask, request, jsonify
from flask_cors import CORS

from accessibility_editor import AccessibilityEditor
from utils import debug_picklify
import base64
from dotenv import load_dotenv

load_dotenv()

try:
   WAVE_API_KEY = os.environ["WAVE_API_KEY"]
   print("WAVE_API_KEY is set to", WAVE_API_KEY)
except KeyError:
   raise KeyError("Please set the WAVE_API_KEY environment variable to your Wave API key.")

app = Flask(__name__)
app.debug = True
CORS(app)

ACCESSIBILITY_API_URL = "https://alphagov.github.io/accessibility-tool-audit/test-cases.html" 
HTTP_EMPTY_RESPONSE = 200

@app.route("/", methods=['GET', 'POST'])
def get_html():
    if request.method == 'POST':
        content = request.json
        url = content["url"]
        html_string = content["html_string"]

        image_arr = content.get("images", None)
        image_bytes_arr = []

        if image_arr:
         image_bytes_arr = [base64.b64decode(image.encode('utf-8')) for image in image_arr]

        dom = parse_html(html_string)
        accessibility_editor = AccessibilityEditor(dom)
        
        accessibility_results = query_accessibility_errors(ACCESSIBILITY_API_URL)

        return process_analysis(
           accessibility_results,
           accessibility_editor
         )
    
    return "", HTTP_EMPTY_RESPONSE

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def query_accessibility_errors(website: str):
  print("Querying WAVE API...")
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

  resp = response.json()

  return resp

def process_analysis(
      results: dict, 
      accessibility_editor: AccessibilityEditor
   ):
   print(f"Results input is of type {type(results)}")
   print(f"Visual analysis URL: {results['statistics']['waveurl']}")
   print(f"Total element count: {results['statistics']['totalelements']}")

   all_errors = list(chain.from_iterable(
      results["categories"][cls]["items"].items()
      for cls in ["error", "alert", "aria", "contrast", "feature", "structure"]
   ))

   new_html_string = ""
   changes_dict = {}
   with tqdm(total = len(all_errors)) as pbar:
      for error_type, error in all_errors:
         pbar.set_description(f"Patching {error_type}...")
         
         try:
            tmp_html, tmp_changes = accessibility_editor.fix(error_type, error)
            new_html_string = tmp_html
            # Add new changes and overwrite existing ones
            for key, val in tmp_changes.items():
               changes_dict[key] = val
         except RuntimeError:
            # TODO: Remove this!
            pass
         
         pbar.update()

   # TODO: Handle alerts!
   # Put responses into JSON
   response_json = {"new_html_string": new_html_string, "html_changes": changes_dict}
   return jsonify(response_json)

if __name__ == "__main__":
   app.run(port=os.environ.get("PORT", 5000))
