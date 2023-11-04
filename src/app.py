from flask import Flask, flash, request, redirect, url_for
from html_modifier import html_accessibility
import sys

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

if __name__ == "__main__":
  app.run()