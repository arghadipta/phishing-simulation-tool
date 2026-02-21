from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import secrets

app = Flask(__name__)

app.secret_key = 'phishing-sim-secret-key-2024-change-in-production'

# Initialize database with new structure
def init_db():
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    # Campaigns table
    c.execute('''CREATE TABLE IF NOT EXISTS campaigns
                 (id TEXT PRIMARY KEY,
                  name TEXT,
                  template TEXT,
                  created_at TEXT)''')
    
    # Targets table (users in each campaign)
    c.execute('''CREATE TABLE IF NOT EXISTS targets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  campaign_id TEXT,
                  email TEXT,
                  name TEXT,
                  token TEXT UNIQUE)''')
    
    # Events table (tracking clicks/submissions)
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  campaign_id TEXT,
                  user_email TEXT,
                  event_type TEXT,
                  timestamp TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    # Get list of campaigns
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    c.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
    campaigns = c.fetchall()
    conn.close()
    
    return render_template('home.html', campaigns=campaigns)

@app.route('/create-campaign')
def create_campaign_page():
    return render_template('create_campaign.html')

@app.route('/create-campaign', methods=['POST'])
def create_campaign():
    # Get form data
    campaign_name = request.form['campaign_name']
    template = request.form['template']
    targets_text = request.form['targets']
    
    # Generate unique campaign ID
    campaign_id = secrets.token_urlsafe(16)
    
    # Parse targets (one per line: "email@test.com Name")
    targets = []
    for line in targets_text.strip().split('\n'):
        if line.strip():
            parts = line.strip().split(' ', 1)
            email = parts[0]
            name = parts[1] if len(parts) > 1 else email.split('@')[0]
            token = secrets.token_urlsafe(32)  # Unique token for each user
            targets.append((campaign_id, email, name, token))
    
    # Save to database
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    # Create campaign
    c.execute("INSERT INTO campaigns (id, name, template, created_at) VALUES (?, ?, ?, ?)",
              (campaign_id, campaign_name, template, datetime.now().isoformat()))
    
    # Add targets
    c.executemany("INSERT INTO targets (campaign_id, email, name, token) VALUES (?, ?, ?, ?)", targets)
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('campaign_detail', campaign_id=campaign_id))

@app.route('/campaign/<campaign_id>')
def campaign_detail(campaign_id):
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    # Get campaign info
    c.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,))
    campaign = c.fetchone()
    
    # Get targets with their tracking links
    c.execute("SELECT email, name, token FROM targets WHERE campaign_id = ?", (campaign_id,))
    targets = c.fetchall()
    
    # Get statistics - FIXED: use 'email' not 'user_email' in targets table
    c.execute("SELECT COUNT(*) FROM targets WHERE campaign_id = ?", (campaign_id,))
    total_targets = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT user_email) FROM events WHERE campaign_id = ? AND event_type = 'clicked'", (campaign_id,))
    clicked_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(DISTINCT user_email) FROM events WHERE campaign_id = ? AND event_type = 'submitted_credentials'", (campaign_id,))
    submitted_count = c.fetchone()[0]
    
    # Get recent events
    c.execute("SELECT * FROM events WHERE campaign_id = ? ORDER BY timestamp DESC LIMIT 20", (campaign_id,))
    events = c.fetchall()
    
    conn.close()
    
    # Calculate percentages
    click_rate = round((clicked_count / total_targets * 100) if total_targets > 0 else 0, 1)
    submit_rate = round((submitted_count / total_targets * 100) if total_targets > 0 else 0, 1)
    
    return render_template('campaign_detail.html',
                         campaign=campaign,
                         targets=targets,
                         total_targets=total_targets,
                         clicked_count=clicked_count,
                         submitted_count=submitted_count,
                         click_rate=click_rate,
                         submit_rate=submit_rate,
                         events=events)

@app.route('/track/<token>')
def track_click(token):
    # Find which campaign and user this token belongs to
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    c.execute("SELECT campaign_id, email FROM targets WHERE token = ?", (token,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return "Invalid tracking link", 404
    
    campaign_id, user_email = result
    
    # Get campaign template
    c.execute("SELECT template FROM campaigns WHERE id = ?", (campaign_id,))
    template = c.fetchone()[0]
    
    # Log the click
    c.execute("INSERT INTO events (campaign_id, user_email, event_type, timestamp) VALUES (?, ?, ?, ?)",
              (campaign_id, user_email, 'clicked', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    # Show the appropriate fake page based on template
    return render_template(f'phishing_{template}.html', token=token)

@app.route('/submit/<token>', methods=['POST'])
def submit_credentials(token):
    # Find campaign and user
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    c.execute("SELECT campaign_id, email FROM targets WHERE token = ?", (token,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return "Invalid token", 404
    
    campaign_id, user_email = result
    
    # Log the submission
    c.execute("INSERT INTO events (campaign_id, user_email, event_type, timestamp) VALUES (?, ?, ?, ?)",
              (campaign_id, user_email, 'submitted_credentials', datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    # Show education page
    return render_template('education.html', user_email=user_email)

@app.route('/reset-database', methods=['POST'])
def reset_database():
    # Delete the database file
    import os
    try:
        os.remove('phishing.db')
    except:
        pass
    
    # Reinitialize
    init_db()
    
    return redirect(url_for('home'))

@app.route('/settings')
def settings():
    # Get database stats
    conn = sqlite3.connect('phishing.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM targets")
    target_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM events")
    event_count = c.fetchone()[0]
    
    conn.close()
    
    return render_template('settings.html', 
                         campaign_count=campaign_count,
                         target_count=target_count,
                         event_count=event_count)

@app.route('/email-templates')
def email_templates():
    return render_template('email_templates.html')

@app.route('/setup-guide')
def setup_guide():
    return render_template('setup_guide.html')

# AFTER:
if __name__ == '__main__':
    # Use environment variable for port (Render requirement)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)