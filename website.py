from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import datetime
import json
import os

app = Flask(__name__)

# File to store guestbook messages
GUESTBOOK_FILE = 'guestbook.json'

# Initialize guestbook if file doesn't exist
if not os.path.exists(GUESTBOOK_FILE):
    with open(GUESTBOOK_FILE, 'w') as f:
        json.dump([], f)

def get_guestbook_messages():
    try:
        with open(GUESTBOOK_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_guestbook_message(messages):
    with open(GUESTBOOK_FILE, 'w') as f:
        json.dump(messages, f)

# Base HTML template with navigation
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Gareje.co.za | {{ title }}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"/>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e12;
            color: #e8edf2;
            line-height: 1.6;
            min-height: 100vh;
            padding: 1.5rem;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        /* Navigation */
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.8rem 0;
            margin-bottom: 2.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            flex-wrap: wrap;
            gap: 1rem;
        }

        .nav-brand {
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #f0f6fc 0%, #8ab4d6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-decoration: none;
        }

        .nav-links {
            display: flex;
            gap: 1.8rem;
            flex-wrap: wrap;
        }

        .nav-links a {
            color: #9aaebf;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: 0.2s;
            padding: 0.3rem 0;
            border-bottom: 2px solid transparent;
        }

        .nav-links a:hover {
            color: #e8edf2;
        }

        .nav-links a.active {
            color: #7bb9ff;
            border-bottom-color: #3b9eff;
        }

        /* Card */
        .card {
            background: linear-gradient(145deg, rgba(18, 22, 26, 0.92), rgba(10, 14, 18, 0.95));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 2.5rem;
            padding: 3rem;
            box-shadow: 
                0 30px 60px -12px rgba(0,0,0,0.9),
                0 0 0 1px rgba(255,255,255,0.05),
                inset 0 1px 0 rgba(255,255,255,0.03);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: -30%;
            right: -20%;
            width: 70%;
            height: 70%;
            background: radial-gradient(circle at 70% 50%, rgba(0, 180, 255, 0.06), transparent 70%);
            pointer-events: none;
            animation: pulse 8s ease-in-out infinite;
        }

        .card::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -20%;
            width: 60%;
            height: 60%;
            background: radial-gradient(circle at 30% 50%, rgba(120, 80, 255, 0.04), transparent 70%);
            pointer-events: none;
            animation: pulse 10s ease-in-out infinite reverse;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }

        .card-content {
            position: relative;
            z-index: 1;
        }

        /* Profile Header */
        .profile-header {
            display: flex;
            flex-wrap: wrap;
            gap: 2.5rem;
            align-items: center;
            margin-bottom: 2.5rem;
        }

        .avatar-wrapper {
            position: relative;
            flex-shrink: 0;
        }

        .avatar-wrapper .ring {
            position: absolute;
            inset: -4px;
            border-radius: 50%;
            padding: 3px;
            background: conic-gradient(from 0deg, #3b9eff, #7b5cff, #3b9eff);
            -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 2px));
            mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #fff calc(100% - 2px));
            animation: spin 6s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .profile-pic {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            display: block;
            background: #1a222a;
            position: relative;
            z-index: 1;
        }

        .online-dot {
            position: absolute;
            bottom: 8px;
            right: 8px;
            width: 16px;
            height: 16px;
            background: #22c55e;
            border-radius: 50%;
            border: 3px solid #0a0e12;
            z-index: 2;
            animation: blink 2s ease-in-out infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .profile-info h1 {
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #f0f6fc 0%, #8ab4d6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.2rem;
        }

        .profile-info .tagline {
            font-size: 1rem;
            font-weight: 400;
            color: #9aaebf;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(34, 197, 94, 0.12);
            padding: 0.2rem 0.9rem;
            border-radius: 40px;
            font-size: 0.7rem;
            font-weight: 500;
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.15);
        }

        /* Buttons */
        .btn-primary {
            display: inline-block;
            padding: 0.6rem 1.8rem;
            background: linear-gradient(135deg, #3b9eff, #7b5cff);
            border: none;
            border-radius: 60px;
            color: #fff;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: 0.3s;
            text-decoration: none;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px -8px rgba(59, 158, 255, 0.4);
        }

        .btn-secondary {
            display: inline-block;
            padding: 0.6rem 1.8rem;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 60px;
            color: #e8edf2;
            font-weight: 500;
            font-size: 0.9rem;
            cursor: pointer;
            transition: 0.3s;
            text-decoration: none;
        }

        .btn-secondary:hover {
            background: rgba(255,255,255,0.08);
            transform: translateY(-2px);
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 2rem 0;
        }

        .stat-card {
            background: rgba(255,255,255,0.02);
            border-radius: 1.2rem;
            padding: 1rem;
            border: 1px solid rgba(255,255,255,0.04);
            text-align: center;
            transition: 0.3s;
        }

        .stat-card:hover {
            background: rgba(255,255,255,0.05);
            border-color: rgba(59, 158, 255, 0.15);
            transform: translateY(-3px);
        }

        .stat-card .stat-icon { font-size: 1.2rem; color: #3b9eff; margin-bottom: 0.2rem; }
        .stat-card .stat-label { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.08em; color: #7f97ab; }
        .stat-card .stat-value { font-size: 1rem; font-weight: 600; color: #eef4f9; }

        /* Social Bar */
        .social-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin: 1.5rem 0;
        }

        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.4rem 1.2rem 0.4rem 1rem;
            border-radius: 60px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            color: #b0c8db;
            text-decoration: none;
            font-size: 0.85rem;
            transition: 0.25s;
        }

        .social-btn i { color: #7bb9ff; }
        .social-btn:hover {
            background: rgba(59, 158, 255, 0.08);
            border-color: rgba(59, 158, 255, 0.2);
            color: #fff;
            transform: translateY(-2px);
        }

        /* Footer */
        .footer-bar {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.8rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.04);
            font-size: 0.75rem;
            color: #5e7485;
            margin-top: 1rem;
        }

        .footer-bar span i { color: #3b9eff; margin-right: 0.3rem; }

        /* Guestbook */
        .guestbook-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            max-width: 500px;
            margin: 1.5rem 0;
        }

        .guestbook-form input,
        .guestbook-form textarea {
            padding: 0.8rem 1rem;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 1rem;
            color: #e8edf2;
            font-family: inherit;
            font-size: 0.9rem;
            transition: 0.3s;
        }

        .guestbook-form input:focus,
        .guestbook-form textarea:focus {
            outline: none;
            border-color: #3b9eff;
            background: rgba(255,255,255,0.06);
        }

        .guestbook-form textarea {
            min-height: 100px;
            resize: vertical;
        }

        .guestbook-messages {
            margin-top: 2rem;
        }

        .message-item {
            background: rgba(255,255,255,0.02);
            padding: 1rem 1.2rem;
            border-radius: 1rem;
            border: 1px solid rgba(255,255,255,0.04);
            margin-bottom: 0.8rem;
        }

        .message-item .msg-name {
            font-weight: 600;
            color: #7bb9ff;
            font-size: 0.9rem;
        }

        .message-item .msg-time {
            font-size: 0.7rem;
            color: #5e7485;
            margin-left: 0.8rem;
        }

        .message-item .msg-text {
            margin-top: 0.3rem;
            color: #c8d9e8;
        }

        /* Contact */
        .contact-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin: 1.5rem 0;
        }

        .contact-item {
            background: rgba(255,255,255,0.02);
            padding: 1.2rem;
            border-radius: 1.2rem;
            border: 1px solid rgba(255,255,255,0.04);
            text-align: center;
            transition: 0.3s;
        }

        .contact-item:hover {
            background: rgba(255,255,255,0.05);
            border-color: rgba(59, 158, 255, 0.15);
            transform: translateY(-3px);
        }

        .contact-item i {
            font-size: 2rem;
            color: #3b9eff;
            margin-bottom: 0.5rem;
        }

        .contact-item .contact-label {
            font-size: 0.7rem;
            color: #7f97ab;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .contact-item .contact-value {
            font-size: 1.1rem;
            font-weight: 500;
            color: #eef4f9;
            margin-top: 0.2rem;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #f0f6fc 0%, #8ab4d6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .section-subtitle {
            color: #9aaebf;
            margin-bottom: 1.5rem;
        }

        .about-content {
            max-width: 90%;
        }

        .about-content p {
            margin-bottom: 1rem;
            color: #c8d9e8;
        }

        .about-content .highlight {
            color: #7bb9ff;
            font-weight: 500;
        }

        .interests-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin: 1.5rem 0;
        }

        .interest-tag {
            background: rgba(59, 158, 255, 0.08);
            padding: 0.4rem 1.2rem;
            border-radius: 60px;
            border: 1px solid rgba(59, 158, 255, 0.1);
            color: #7bb9ff;
            font-size: 0.9rem;
        }

        .btn-group {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }

        /* Responsive */
        @media (max-width: 820px) {
            .card { padding: 1.8rem; border-radius: 2rem; }
            .profile-header { flex-direction: column; align-items: flex-start; gap: 1.2rem; }
            .profile-info h1 { font-size: 2rem; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .contact-info { grid-template-columns: 1fr; }
            .about-content { max-width: 100%; }
            .navbar { flex-direction: column; align-items: flex-start; }
            .nav-links { gap: 1rem; }
        }

        @media (max-width: 480px) {
            .profile-pic { width: 100px; height: 100px; }
            .stats-grid { grid-template-columns: 1fr 1fr; gap: 0.6rem; }
            .stat-card { padding: 0.7rem; }
            .card { padding: 1.2rem; border-radius: 1.5rem; }
            .social-btn { padding: 0.3rem 0.9rem; font-size: 0.75rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <a href="/" class="nav-brand">Gareje.co.za</a>
            <div class="nav-links">
                <a href="/" class="{% if active == 'home' %}active{% endif %}">Home</a>
                <a href="/about" class="{% if active == 'about' %}active{% endif %}">About Me</a>
                <a href="/guestbook" class="{% if active == 'guestbook' %}active{% endif %}">Guestbook</a>
                <a href="/contact" class="{% if active == 'contact' %}active{% endif %}">Contact</a>
            </div>
        </nav>

        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <div class="card">
        <div class="card-content">
            <div class="profile-header">
                <div class="avatar-wrapper">
                    <div class="ring"></div>
                    <img src="/static/profile.jpg" alt="Gareje" class="profile-pic" />
                    <div class="online-dot"></div>
                </div>
                <div class="profile-info">
                    <h1>Tshegofatso Isaac Gareje</h1>
                    <div class="tagline">
                        Self-Taught Developer & South African Navy Member
                        <span class="badge"><i class="fas fa-circle"></i> Available</span>
                    </div>
                </div>
            </div>

            <p style="color: #c8d9e8; font-size: 1.05rem; max-width: 85%; margin-bottom: 1.5rem;">
                Welcome to my digital portfolio. From a first-year dropout to a self-taught programmer creating this very website
                using Python. I am currently serving in the <span class="highlight">SANDF</span> and chasing my passion for technology.
            </p>

            <a href="/about" class="btn-primary"><i class="fas fa-book-open"></i> Read My Story</a>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-map-pin"></i></div>
                    <div class="stat-label">Location</div>
                    <div class="stat-value">South Africa</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-code"></i></div>
                    <div class="stat-label">Experience</div>
                    <div class="stat-value">3+ Years</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-cogs"></i></div>
                    <div class="stat-label">Focus</div>
                    <div class="stat-value">Web & Backend</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-rocket"></i></div>
                    <div class="stat-label">Status</div>
                    <div class="stat-value">Live on Render</div>
                </div>
            </div>

            <div class="social-bar">
                <a href="#" class="social-btn"><i class="fab fa-github"></i> GitHub</a>
                <a href="#" class="social-btn"><i class="fab fa-linkedin-in"></i> LinkedIn</a>
                <a href="#" class="social-btn"><i class="fab fa-x-twitter"></i> Twitter</a>
                <a href="#" class="social-btn"><i class="fas fa-envelope"></i> Email</a>
            </div>

            <div class="footer-bar">
                <span><i class="fas fa-server"></i> Deployed on Render</span>
                <span><i class="far fa-clock"></i> {{ time }}</span>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, title="Home", active="home", content=content.replace("{{ time }}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

@app.route('/about')
def about():
    content = """
    <div class="card">
        <div class="card-content">
            <h1 class="section-title">My Journey</h1>
            
            <div class="about-content">
                <p>
                    <strong>Where I'm From:</strong> I was born and raised in North West, Mafikeng, and I am proud to be a Tswana speaker. 
                    I started my tertiary education at Richfield College in Durban, but I made the tough decision to drop out in my first year.
                </p>
                
                <p>
                    <strong>The Pivot:</strong> Instead of giving up, I taught myself Python and web development. 
                    This website is a testament to that self-discipline. I believe that the best classroom is the internet itself.
                </p>
                
                <p>
                    <strong>Current Role:</strong> I am currently based in the beautiful Western Cape, specifically Gordons Bay, 
                    proudly working for the South African Navy (SANDF).
                </p>
            </div>

            <h2 style="color: #e8edf2; font-size: 1.3rem; margin-top: 2rem; margin-bottom: 0.8rem;">What I'm Interested In</h2>
            
            <div class="interests-list">
                <span class="interest-tag"><i class="fas fa-globe"></i> Web Development</span>
                <span class="interest-tag"><i class="fab fa-apple"></i> macOS Apps</span>
                <span class="interest-tag"><i class="fas fa-brain"></i> Artificial Intelligence</span>
            </div>

            <p style="color: #9aaebf; font-size: 0.9rem; margin-top: 0.5rem;">
                Building interactive sites like this one from scratch • Creating native applications for Apple devices • Exploring machine learning and neural networks
            </p>

            <div class="btn-group">
                <a href="/contact" class="btn-primary"><i class="fas fa-envelope"></i> Get In Touch</a>
                <a href="/" class="btn-secondary"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>

            <div class="footer-bar">
                <span><i class="fas fa-server"></i> Deployed on Render</span>
                <span><i class="far fa-clock"></i> {{ time }}</span>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, title="About Me", active="about", content=content.replace("{{ time }}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    messages = get_guestbook_messages()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()
        if name and message:
            messages.append({
                'name': name,
                'message': message,
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_guestbook_message(messages)
        return redirect(url_for('guestbook'))
    
    messages_html = ""
    if messages:
        for msg in messages:
            messages_html += f"""
            <div class="message-item">
                <div class="msg-name">{msg['name']} <span class="msg-time">{msg['time']}</span></div>
                <div class="msg-text">{msg['message']}</div>
            </div>
            """
    else:
        messages_html = '<p style="color: #5e7485;">No messages yet. Be the first to leave a comment!</p>'
    
    content = f"""
    <div class="card">
        <div class="card-content">
            <h1 class="section-title">Guestbook</h1>
            <p class="section-subtitle">Leave a comment or message for me! (Saved on the server)</p>
            
            <h3 style="color: #e8edf2; margin-bottom: 0.8rem; font-size: 1.1rem;">Write a Comment</h3>
            
            <form method="POST" class="guestbook-form">
                <input type="text" name="name" placeholder="Your Name" required />
                <textarea name="message" placeholder="Your Message..." required></textarea>
                <button type="submit" class="btn-primary" style="align-self: flex-start;"><i class="fas fa-pen"></i> Post Comment</button>
            </form>
            
            <div class="guestbook-messages">
                {messages_html}
            </div>
            
            <div class="footer-bar">
                <span><i class="fas fa-server"></i> Deployed on Render</span>
                <span><i class="far fa-clock"></i> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, title="Guestbook", active="guestbook", content=content)

@app.route('/contact')
def contact():
    content = """
    <div class="card">
        <div class="card-content">
            <h1 class="section-title">Contact Me</h1>
            <p class="section-subtitle">Feel free to reach out for opportunities, collaborations, or just to say hi!</p>
            
            <div class="contact-info">
                <div class="contact-item">
                    <i class="fab fa-whatsapp"></i>
                    <div class="contact-label">WhatsApp</div>
                    <div class="contact-value">062 483 6868</div>
                </div>
                <div class="contact-item">
                    <i class="fab fa-tiktok"></i>
                    <div class="contact-label">TikTok</div>
                    <div class="contact-value">@Isaac_bae</div>
                </div>
                <div class="contact-item">
                    <i class="fas fa-envelope"></i>
                    <div class="contact-label">Email</div>
                    <div class="contact-value">gareje@proton.me</div>
                </div>
                <div class="contact-item">
                    <i class="fab fa-github"></i>
                    <div class="contact-label">GitHub</div>
                    <div class="contact-value">github.com/isaacbae</div>
                </div>
            </div>
            
            <div class="btn-group">
                <a href="https://wa.me/27624836868" class="btn-primary"><i class="fab fa-whatsapp"></i> WhatsApp Me</a>
                <a href="/" class="btn-secondary"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>
            
            <div class="footer-bar">
                <span><i class="fas fa-server"></i> Deployed on Render</span>
                <span><i class="far fa-clock"></i> {{ time }}</span>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, title="Contact", active="contact", content=content.replace("{{ time }}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
