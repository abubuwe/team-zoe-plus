import os
import requests
import os
from itertools import chain

from tqdm import tqdm
from html_modifier import parse_html
from flask import Flask, request

from accessibility_editor import AccessibilityEditor
from utils import debug_picklify
import base64
from dotenv import load_dotenv

load_dotenv()

try:
   WAVE_API_KEY = os.environ["WAVE_API_KEY"]
except KeyError:
   raise KeyError("Please set the WAVE_API_KEY environment variable to your Wave API key.")

app = Flask(__name__)
app.debug = True

ACCESSIBILITY_API_URL = "https://alphagov.github.io/accessibility-tool-audit/test-cases.html" 
HTTP_EMPTY_RESPONSE = 200
WAVE_API_KEY = os.getenv("WAVE_API_KEY")

@app.route("/", methods=['POST'])
def get_html():
   if request.method != "POST":
      return "", HTTP_EMPTY_RESPONSE
    
   content = request.json
   url = content["url"]
   html_string = content["html_string"]
   
   acc_errors = query_accessibility_errors(url)
   dom = parse_html(html_string)

   accessibility_editor = AccessibilityEditor(dom)
   return process_analysis(acc_errors, accessibility_editor)
    
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

def process_analysis(
      results: dict, 
      accessibility_editor: AccessibilityEditor
   ):
   print(f"Visual analysis URL: {results['statistics']['waveurl']}")
   print(f"Total element count: {results['statistics']['totalelements']}")

   all_errors = list(chain.from_iterable(
      results["categories"][cls]["items"].items()
      for cls in ["error", "alert", "aria", "contrast", "feature", "structure"]
   ))

   with tqdm(total = len(all_errors)) as pbar:
      for error_type, error in all_errors:
         pbar.set_description(f"Patching {error_type}...")
         accessibility_editor.fix(error_type, error)
         pbar.update()

   return accessibility_editor.get_page()

if __name__ == "__main__":
   app.run(port=os.environ.get("PORT", 5000))
