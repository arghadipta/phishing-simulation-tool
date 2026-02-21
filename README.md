# 🎣 Phishing Simulation Tool

A full-stack web application for conducting security awareness training through realistic phishing simulations. Built with Flask, SQLite, and vanilla JavaScript.

## 🎯 Live Demo

**[View Live Demo →](https://your-app.onrender.com)** *(Coming soon)*

> **Note:** The app may take 30-60 seconds to wake up from sleep on first visit (free tier limitation).

## ✨ Features

- **Campaign Management**: Create and manage multiple phishing simulation campaigns
- **Multiple Templates**: 3 realistic phishing scenarios with varying difficulty levels
  - Password Reset (Easy)
  - Package Delivery (Medium)
  - HR Document Review (Medium)
- **Real-time Tracking**: Monitor who clicks links and submits credentials
- **Analytics Dashboard**: Visualize click rates, submission rates, and user behavior
- **Educational Feedback**: Immediate learning experience for caught users
- **Email Template Generator**: Ready-to-use phishing email templates
- **Database Management**: Reset and manage campaign data

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Template Engine**: Jinja2
- **Deployment**: Render

## 🚀 Local Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/phishing-simulation-tool.git
   cd phishing-simulation-tool
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Run the application**
```bash
   python app.py
```

4. **Access the app**
```
   Open browser: http://localhost:5000
```

## 📖 Usage

### Creating a Campaign

1. Click **"Create New Campaign"** on the dashboard
2. Enter campaign details:
   - Name (e.g., "Q1 2024 Security Training")
   - Select phishing template
   - Add target emails (one per line: `email@domain.com Name`)
3. Click **"Create Campaign"**
4. Copy tracking links from campaign detail page
5. Send phishing emails to targets using provided templates
6. Monitor results in real-time

### Available Templates

- **Password Reset**: Urgent password expiration scenario
- **Package Delivery**: Failed delivery notification
- **HR Document**: Employee handbook acknowledgment

## 📊 Analytics

The dashboard provides:
- Total targets
- Click rate percentage
- Credential submission rate
- Activity timeline
- Visual progress bars

## ⚠️ Legal & Ethical Usage

**CRITICAL:** This tool is for **authorized security awareness training only**.

### Requirements:
- ✅ Written authorization from organization leadership
- ✅ Informed consent from participants
- ✅ Compliance with all applicable laws
- ✅ Clear educational purpose

### Prohibited Uses:
- ❌ Unauthorized testing
- ❌ Malicious purposes
- ❌ Storing real credentials
- ❌ Targeting external organizations

## 🔒 Security Features

- No actual credentials are stored (only event metadata)
- Unique cryptographic tokens for tracking
- SQL injection protection via parameterized queries
- Debug mode disabled in production
- Privacy-focused design

## 🗂️ Project Structure
```
phishing-simulation-tool/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                     # Git ignore rules
└── templates/                     # HTML templates
    ├── home.html
    ├── create_campaign.html
    ├── campaign_detail.html
    ├── education.html
    ├── email_templates.html
    ├── setup_guide.html
    ├── settings.html
    └── phishing_*.html            # Phishing page templates
```

## 🎓 Learning Outcomes

This project demonstrates:
- Full-stack web development
- RESTful routing with Flask
- Database design and SQL queries
- User session tracking
- Security-focused development
- Ethical considerations in cybersecurity
- Production deployment

## 🔮 Future Enhancements

- [ ] User authentication system
- [ ] Export reports to PDF
- [ ] Email scheduling/automation
- [ ] More phishing templates
- [ ] Multi-language support
- [ ] Team collaboration features

## 👤 Author

**Your Name**
- GitHub: [@arghadipta](https://github.com/arghadipta)
- LinkedIn:(https://linkedin.com/in/arghadipta)

## 🙏 Acknowledgments

Built as a cybersecurity educational project to address real-world phishing awareness training needs.

---

⭐ **If you found this project useful, please consider giving it a star!**