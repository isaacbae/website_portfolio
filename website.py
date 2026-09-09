from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gareje - Portfolio</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0a0a0a;
            color: #ffffff;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            background: rgba(20, 20, 20, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.05);
            position: relative;
            overflow: hidden;
        }
        
        .bg-blur {
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background-image: url('/static/profile.jpg');
            background-size: cover;
            background-position: center;
            filter: blur(30px);
            opacity: 0.15;
            z-index: 0;
        }
        
        .content {
            position: relative;
            z-index: 1;
        }
        
        .profile-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .profile-pic {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #00d4ff;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.2);
            margin-bottom: 20px;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #7b2ffc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 5px;
        }
        
        .title {
            font-size: 1.1rem;
            color: #888;
            font-weight: 300;
            letter-spacing: 2px;
        }
        
        .divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #00d4ff, transparent);
            margin: 30px 0;
            opacity: 0.3;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 30px 0;
        }
        
        .info-item {
            background: rgba(255, 255, 255, 0.03);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        
        .info-item:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(0, 212, 255, 0.2);
            transform: translateY(-2px);
        }
        
        .info-item .label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #666;
            margin-bottom: 5px;
        }
        
        .info-item .value {
            font-size: 1.1rem;
            font-weight: 500;
            color: #eee;
        }
        
        .bio {
            font-size: 1.05rem;
            line-height: 1.8;
            color: #ccc;
            text-align: center;
            margin: 20px 0;
        }
        
        .status-badge {
            display: inline-block;
            background: rgba(0, 212, 255, 0.1);
            color: #00d4ff;
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.8rem;
            border: 1px solid rgba(0, 212, 255, 0.2);
            margin-top: 10px;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            font-size: 0.8rem;
            color: #555;
        }
        
        @media (max-width: 600px) {
            .container {
                padding: 25px;
            }
            .info-grid {
                grid-template-columns: 1fr;
            }
            h1 {
                font-size: 2rem;
            }
            .profile-pic {
                width: 120px;
                height: 120px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="bg-blur"></div>
        <div class="content">
            <div class="profile-section">
                <img src="/static/profile.jpg" alt="Profile" class="profile-pic">
                <h1>Gareje</h1>
                <div class="title">Software Developer</div>
                <div class="status-badge">🟢 Available for work</div>
            </div>
            
            <div class="bio">
                Passionate about building elegant solutions and bringing ideas to life through code.
            </div>
            
            <div class="divider"></div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">📍 Location</div>
                    <div class="value">South Africa</div>
                </div>
                <div class="info-item">
                    <div class="label">💼 Experience</div>
                    <div class="value">3+ Years</div>
                </div>
                <div class="info-item">
                    <div class="label">🛠️ Skills</div>
                    <div class="value">Python, Flask, JavaScript</div>
                </div>
                <div class="info-item">
                    <div class="label">🚀 Status</div>
                    <div class="value">Live on Render</div>
                </div>
            </div>
            
            <div class="footer">
                <p>© 2026 Gareje. Built with Flask & deployed on Render</p>
                <p style="margin-top: 5px; font-size: 0.7rem;">🟢 Server time: {{ time }}</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML, time=now)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
