import json
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, Response

app = Flask(__name__)
COMMENTS_FILE = "comments.json"

# Initialize comments file
if not os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, "w") as f:
        json.dump([], f)

# ---------- HTML/CSS/JS (SAME AS BEFORE) ----------
HTML_CONTENT = """... (insert your exact HTML_CONTENT string from your previous code here) ..."""

# ---------- ROUTES ----------
@app.route('/')
def home():
    return Response(HTML_CONTENT, mimetype='text/html')

@app.route('/api/comments', methods=['GET'])
def get_comments():
    with open(COMMENTS_FILE, "r") as f:
        comments = json.load(f)
    return jsonify(comments)

@app.route('/api/comments', methods=['POST'])
def post_comment():
    data = request.json
    new_comment = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'message': data['message'],
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'ip': request.headers.get('CF-Connecting-IP', 'Unknown'),
        'removed': False
    }
    with open(COMMENTS_FILE, "r") as f:
        comments = json.load(f)
    comments.append(new_comment)
    with open(COMMENTS_FILE, "w") as f:
        json.dump(comments, f, indent=4)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
