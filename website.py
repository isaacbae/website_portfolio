from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Gareje.co.za | Portfolio</title>
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
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }

        .card {
            max-width: 1000px;
            width: 100%;
            background: linear-gradient(145deg, rgba(18, 22, 26, 0.92), rgba(10, 14, 18, 0.95));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 3rem;
            padding: 3rem;
            box-shadow: 
                0 30px 60px -12px rgba(0,0,0,0.9),
                0 0 0 1px rgba(255,255,255,0.05),
                inset 0 1px 0 rgba(255,255,255,0.03);
            position: relative;
            overflow: hidden;
        }

        /* Animated gradient orb */
        .card::before {
            content: '';
            position: absolute;
            top: -30%;
            right: -20%;
            width: 70%;
            height: 70%;
            background: radial-gradient(circle at 70% 50%, rgba(0, 180, 255, 0.08), transparent 70%);
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
            background: radial-gradient(circle at 30% 50%, rgba(120, 80, 255, 0.06), transparent 70%);
            pointer-events: none;
            animation: pulse 10s ease-in-out infinite reverse;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.5; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.1); }
        }

        /* --- header / profile --- */
        .profile-header {
            display: flex;
            flex-wrap: wrap;
            gap: 2.5rem;
            align-items: center;
            margin-bottom: 2.5rem;
            position: relative;
            z-index: 1;
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
            width: 140px;
            height: 140px;
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
            width: 18px;
            height: 18px;
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
            font-size: 3rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #f0f6fc 0%, #8ab4d6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.3rem;
        }

        .profile-info .title-row {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 1rem;
        }

        .profile-info .tagline {
            font-size: 1.15rem;
            font-weight: 400;
            color: #9aaebf;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(34, 197, 94, 0.12);
            padding: 0.25rem 1rem;
            border-radius: 40px;
            font-size: 0.75rem;
            font-weight: 500;
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.15);
        }

        .badge i {
            font-size: 0.6rem;
        }

        /* --- about --- */
        .about-section {
            position: relative;
            z-index: 1;
            margin-bottom: 2.5rem;
        }

        .about-section p {
            font-size: 1.1rem;
            color: #c8d9e8;
            max-width: 85%;
            line-height: 1.8;
        }

        .highlight {
            color: #7bb9ff;
            font-weight: 500;
        }

        /* --- stats grid --- */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.2rem;
            margin-bottom: 2.5rem;
            position: relative;
            z-index: 1;
        }

        .stat-card {
            background: rgba(255,255,255,0.02);
            border-radius: 1.5rem;
            padding: 1.2rem 1.2rem;
            border: 1px solid rgba(255,255,255,0.04);
            transition: all 0.3s ease;
            text-align: center;
        }

        .stat-card:hover {
            background: rgba(255,255,255,0.05);
            border-color: rgba(59, 158, 255, 0.15);
            transform: translateY(-3px);
            box-shadow: 0 8px 25px -8px rgba(0,0,0,0.4);
        }

        .stat-card .stat-icon {
            font-size: 1.4rem;
            color: #3b9eff;
            margin-bottom: 0.3rem;
        }

        .stat-card .stat-label {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #7f97ab;
            margin-bottom: 0.15rem;
        }

        .stat-card .stat-value {
            font-size: 1.15rem;
            font-weight: 600;
            color: #eef4f9;
        }

        /* --- social bar --- */
        .social-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.8rem;
            margin-bottom: 2.2rem;
            position: relative;
            z-index: 1;
        }

        .social-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.5rem 1.4rem 0.5rem 1.2rem;
            border-radius: 60px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            color: #b0c8db;
            text-decoration: none;
            font-size: 0.9rem;
            transition: all 0.25s ease;
        }

        .social-btn i {
            font-size: 1.1rem;
            width: 1.2rem;
            color: #7bb9ff;
            transition: 0.2s;
        }

        .social-btn:hover {
            background: rgba(59, 158, 255, 0.08);
            border-color: rgba(59, 158, 255, 0.2);
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px -8px rgba(59, 158, 255, 0.15);
        }

        .social-btn:hover i {
            color: #3b9eff;
        }

        /* --- footer --- */
        .footer-bar {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.8rem;
            padding-top: 1.8rem;
            border-top: 1px solid rgba(255,255,255,0.04);
            position: relative;
            z-index: 1;
            font-size: 0.8rem;
            color: #5e7485;
        }

        .footer-bar span i {
            color: #3b9eff;
            margin-right: 0.4rem;
        }

        /* --- responsiveness --- */
        @media (max-width: 820px) {
            .card { padding: 2rem 1.5rem; border-radius: 2rem; }
            .profile-header { flex-direction: column; align-items: flex-start; gap: 1.2rem; }
            .profile-info h1 { font-size: 2.4rem; }
            .about-section p { max-width: 100%; font-size: 1rem; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 480px) {
            .profile-pic { width: 110px; height: 110px; }
            .profile-info h1 { font-size: 2rem; }
            .stats-grid { grid-template-columns: 1fr 1fr; gap: 0.8rem; }
            .stat-card { padding: 0.9rem; }
            .social-btn { padding: 0.4rem 1rem 0.4rem 0.8rem; font-size: 0.8rem; }
            .footer-bar { flex-direction: column; align-items: center; text-align: center; }
        }
    </style>
</head>
<body>

<div class="card">
    <!-- Profile Header -->
    <div class="profile-header">
        <div class="avatar-wrapper">
            <div class="ring"></div>
            <img src="/static/profile.jpg" alt="Gareje" class="profile-pic" />
            <div class="online-dot"></div>
        </div>
        <div class="profile-info">
            <h1>Gareje</h1>
            <div class="title-row">
                <span class="tagline">Software Developer</span>
                <span class="badge"><i class="fas fa-circle"></i> Available for work</span>
            </div>
        </div>
    </div>

    <!-- About -->
    <div class="about-section">
        <p>
            Passionate about crafting <span class="highlight">clean, user-friendly</span> digital experiences. 
            I build with Python, Flask, and modern front-end tools to bring ideas to life.
        </p>
    </div>

    <!-- Stats -->
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
            <div class="stat-value">Web &amp; Backend</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><i class="fas fa-rocket"></i></div>
            <div class="stat-label">Status</div>
            <div class="stat-value">Live on Render</div>
        </div>
    </div>

    <!-- Social Links -->
    <div class="social-bar">
        <a href="#" class="social-btn"><i class="fab fa-github"></i> GitHub</a>
        <a href="#" class="social-btn"><i class="fab fa-linkedin-in"></i> LinkedIn</a>
        <a href="#" class="social-btn"><i class="fab fa-x-twitter"></i> Twitter</a>
        <a href="#" class="social-btn"><i class="fas fa-envelope"></i> Email</a>
    </div>

    <!-- Footer -->
    <div class="footer-bar">
        <span><i class="fas fa-server"></i> Deployed on Render</span>
        <span><i class="far fa-clock"></i> {{ time }}</span>
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
