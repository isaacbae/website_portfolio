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

# ---------- HTML/CSS/JS (FULL WEBSITE) ----------
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tshegofatso Isaac Gareje | Portfolio</title>
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Tshegofatso Isaac Gareje | Portfolio" />
    <meta property="og:description" content="Self-Taught Developer & South African Navy Member. Building the future with Python, Web Dev, macOS Apps & AI." />
    <meta property="og:image" content="https://gareje.co.za/profile.jpg" />
    <meta property="og:url" content="https://gareje.co.za" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Tshegofatso Isaac Gareje | Portfolio" />
    <meta name="twitter:description" content="Self-Taught Developer & South African Navy Member." />
    <meta name="twitter:image" content="https://gareje.co.za/profile.jpg" />
    <style>
        :root {
            --navy: #000080;
            --purple: #4b0082;
            --accent: #ffcc00;
        }
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #fff;
            overflow-x: hidden;
        }
        .bg-blur {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background-image: url('profile.jpg');
            background-size: cover;
            background-position: center;
            filter: blur(15px) brightness(0.4) saturate(1.2);
            transform: scale(1.1);
        }
        .bg-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(120deg, rgba(75, 0, 130, 0.6), rgba(0, 0, 128, 0.7), rgba(75, 0, 130, 0.6));
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        nav {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(10px);
            padding: 20px;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            border-bottom: 2px solid rgba(255, 204, 0, 0.3);
        }
        nav a {
            color: #fff;
            text-decoration: none;
            margin: 0 20px;
            font-size: 1.2rem;
            font-weight: bold;
            position: relative;
            transition: color 0.3s;
        }
        nav a:hover { color: var(--accent); }
        nav a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -5px;
            left: 0;
            background-color: var(--accent);
            transition: width 0.3s;
        }
        nav a:hover::after { width: 100%; }
        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 40px;
            background: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease;
        }
        .show { opacity: 1; transform: translateY(0); }
        img.profile-pic {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            object-fit: cover;
            border: 5px solid var(--accent);
            box-shadow: 0 0 20px rgba(255, 204, 0, 0.5);
            animation: pulse 3s infinite;
            margin-bottom: 20px;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 204, 0, 0.7); }
            70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(255, 204, 0, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 204, 0, 0); }
        }
        h1 { margin-bottom: 10px; font-size: 3rem; letter-spacing: 2px; text-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        h2 { color: #ccccff; font-weight: 300; margin-bottom: 30px; }
        p { line-height: 1.8; font-size: 1.1rem; text-align: left; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            background: linear-gradient(45deg, var(--accent), #ffaa00);
            color: #000080;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            margin: 10px;
            box-shadow: 0 5px 20px rgba(255, 204, 0, 0.4);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(255, 204, 0, 0.6); }
        .btn-tiktok { background: #000; color: #fff; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s, border-color 0.3s;
        }
        .card:hover { transform: scale(1.05); border-color: var(--accent); background: rgba(255, 255, 255, 0.15); }
        .comment-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 15px;
            margin-top: 40px;
            text-align: left;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            border: none;
            background: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            box-sizing: border-box;
        }
        #submit-btn { width: 100%; }
        .comment {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            border-left: 4px solid var(--accent);
        }
        .comment h4 { margin: 0 0 5px 0; color: var(--accent); }
        .comment small { color: #aaa; }
        .comment p { margin: 10px 0 0 0; font-size: 1rem; }
        .comment.removed {
            border-left: 4px solid #ff3333;
            opacity: 0.7;
            font-style: italic;
        }
        .comment.removed h4 { color: #ff3333; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="bg-blur"></div>
    <div class="bg-overlay"></div>
    <nav>
        <a href="#home" onclick="showPage('home')">Home</a>
        <a href="#about" onclick="showPage('about')">About Me</a>
        <a href="#comments" onclick="showPage('comments')">Guestbook</a>
        <a href="#contact" onclick="showPage('contact')">Contact</a>
    </nav>
    <div id="home" class="container">
        <img src="profile.jpg" class="profile-pic" alt="Tshegofatso Isaac Gareje">
        <h1>Tshegofatso Isaac Gareje</h1>
        <h2>Self-Taught Developer & South African Navy Member</h2>
        <p>
            Welcome to my digital portfolio. From a first-year dropout to a self-taught programmer creating 
            this very website using Python. I am currently serving in the SANDF and chasing my passion 
            for technology.
        </p>
        <a href="#about" class="btn" onclick="showPage('about')">Read My Story</a>
    </div>
    <div id="about" class="container hidden">
        <h1>My Journey</h1>
        <p><strong>Where I'm From:</strong> I was born and raised in North West, Mafikeng, and I am proud to be a Tswana speaker. I started my tertiary education at Richfield College in Durban, but I made the tough decision to drop out in my first year.</p>
        <p><strong>The Pivot:</strong> Instead of giving up, I taught myself Python and web development. This website is a testament to that self-discipline. I believe that the best classroom is the internet itself.</p>
        <p><strong>Current Role:</strong> I am currently based in the beautiful Western Cape, specifically Gordons Bay, proudly working for the South African Navy (SANDF).</p>
        <h2>What I'm Interested In</h2>
        <div class="grid">
            <div class="card"><h3>Web Development</h3><p>Building interactive sites like this one from scratch.</p></div>
            <div class="card"><h3>macOS Apps</h3><p>Creating native applications for Apple devices.</p></div>
            <div class="card"><h3>Artificial Intelligence</h3><p>Exploring machine learning and neural networks.</p></div>
        </div>
        <a href="#contact" class="btn" onclick="showPage('contact')">Get In Touch</a>
    </div>
    <div id="comments" class="container hidden">
        <h1>Guestbook</h1>
        <p>Leave a comment or message for me! (Saved on the server)</p>
        <div class="comment-box">
            <h3>Write a Comment</h3>
            <input type="text" id="name" placeholder="Your Name">
            <textarea id="message" placeholder="Your Message..." rows="4"></textarea>
            <button id="submit-btn" class="btn" onclick="postComment()">Post Comment</button>
        </div>
        <div id="comment-list"></div>
    </div>
    <div id="contact" class="container hidden">
        <h1>Contact Me</h1>
        <p>Feel free to reach out for opportunities, collaborations, or just to say hi!</p>
        <a href="https://wa.me/27624836868" class="btn">WhatsApp: 062 483 6868</a>
        <a href="https://www.tiktok.com/@Isaac_bae" target="_blank" class="btn btn-tiktok">TikTok: @Isaac_bae</a>
    </div>
    <script>
        function showPage(pageId) {
            const pages = document.querySelectorAll('.container');
            pages.forEach(page => { page.classList.add('hidden'); page.classList.remove('show'); });
            const target = document.getElementById(pageId);
            target.classList.remove('hidden');
            setTimeout(() => target.classList.add('show'), 50);
            window.scrollTo(0, 0);
        }
        window.onload = function() { loadComments(); showPage('home'); };
        async function loadComments() {
            const response = await fetch('/api/comments');
            const comments = await response.json();
            const list = document.getElementById('comment-list');
            list.innerHTML = '';
            comments.forEach(comment => {
                const div = document.createElement('div');
                div.className = comment.removed ? 'comment removed' : 'comment';
                let displayMessage = comment.removed ? "This message was removed by the user." : comment.message;
                div.innerHTML = `<h4>${comment.name}</h4><small>${comment.date}</small><p>${displayMessage}</p>`;
                list.appendChild(div);
            });
        }
        async function postComment() {
            const name = document.getElementById('name').value;
            const message = document.getElementById('message').value;
            if (!name || !message) { alert("Please fill in both name and message!"); return; }
            const response = await fetch('/api/comments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, message: message })
            });
            if (response.ok) {
                document.getElementById('name').value = '';
                document.getElementById('message').value = '';
                loadComments();
            } else { alert('Failed to post comment.'); }
        }
    </script>
</body>
</html>
"""

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
