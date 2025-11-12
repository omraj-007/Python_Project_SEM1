# 🇮🇳 PM Internship Recommendation Engine

Current Date and Time: 2025-01-27 19:18:15 UTC | User: Om Raj Singh

---

## 🚀 Technology & Links

🇮🇳 [PM Internship Scheme - Government of India](https://pminternship.mca.gov.in/)

💻 Tech Stack:

- [Python 3.8+](https://python.org) - Backend Development
- [Flask 2.0+](https://flask.palletsprojects.com/) - Web Framework
- [JavaScript ES6+](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Frontend Logic
- [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML) & [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) - UI Design
- [Scikit-Learn](https://scikit-learn.org/) - Machine Learning
- [TF-IDF Algorithm](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) - Recommendation Engine

🏆 Project Status: [Hackathon Ready](https://github.com/Om Raj Singh) ✅

## 🎯 Project Overview

An intelligent recommendation system for the Prime Minister's Internship Scheme that matches students with relevant internship opportunities based on their educational background, skills, and preferences. Built for hackathon excellence with real-world application potential.

## ✨ Key Features

### 🎓 Smart Education-Based Matching

- 12+ Education Fields supported (Computer Science, Mechanical, Civil, Commerce, etc.)
- Dynamic skill suggestions based on selected field
- Field-specific internship recommendations

### 🤖 AI-Powered Recommendation Engine

- TF-IDF Algorithm for intelligent matching
- Multi-criteria filtering (location, stipend, skills)
- Personalized scoring system

### 🏢 Comprehensive Database

- 200+ PM Internship opportunities
- 50+ Top Indian companies (TCS, Infosys, Google, Microsoft, Tata Motors, etc.)
- Real company career page integrations

### 🎨 Professional UI/UX

- Responsive design for all devices
- Government PM Scheme branding
- Interactive skill selection
- Real-time form validation

## 🛠️ Technology Stack

### Backend

- Python 3.8+
- Flask 2.0+ - REST API framework
- Pandas - Data processing
- Scikit-learn - Machine learning algorithms
- Flask-CORS - Cross-origin resource sharing

### Frontend

- HTML5 - Semantic markup
- CSS3 - Modern styling with gradients & animations
- JavaScript ES6+ - Interactive functionality
- Font Awesome - Professional icons
- Responsive Grid - Mobile-first design

### Data

- CSV Database - 200+ internship records
- Real company URLs - Direct career page links
- Government portal integration

## 📁 Project Structure

```
pm-internship-engine/
├── backend/
│   ├── app.py                 # Flask application
│   ├── recommendation_engine.py  # ML recommendation logic
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── style.css             # Styling
│   ├── mobile.css            # Mobile responsiveness
│   └── script.js             # JavaScript functionality
├── data/
│   └── internship.csv        # Internship database (200+ records)
└── README.md                 # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser
- Internet connection

### Installation & Setup

1. Clone the repository

```bash
git clone https://github.com/Om Raj Singh/pm-internship-engine.git
cd pm-internship-engine
```

2. Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

3. Start the Flask backend

```bash
python app.py
```

4. Open the frontend

```bash
cd ../frontend
# Open index.html in your browser or use live server
```

5. Access the application

- Frontend: `http://localhost:3000` (or your live server port)
- Backend API: `http://localhost:5000`

## 🎯 How It Works

### 1. User Input

- Select education field (Computer Science, Mechanical, etc.)
- Choose relevant skills (auto-updated based on field)
- Set location preference
- Specify minimum stipend

### 2. AI Processing

- TF-IDF vectorization of user profile
- Cosine similarity calculation with internship database
- Multi-criteria scoring algorithm
- Top-N recommendation selection

### 3. Results & Application

- Display personalized internship recommendations
- Show match percentage for each opportunity
- Direct redirect to company career pages
- PM Internship portal integration

## 📊 Database Coverage

### Education Fields (12)

- Computer Science/IT
- Electronics/Electrical Engineering
- Mechanical Engineering
- Civil Engineering
- Business/Management
- Commerce/Finance/Accounting
- Arts/Humanities/Literature
- Design/Fine Arts/Creative
- Media/Communication/Journalism
- Marketing/Sales/Digital Marketing
- Human Resources/Psychology
- Operations/Supply Chain/Logistics

### Companies (50+)

- Technology: TCS, Infosys, Google, Microsoft, Amazon, IBM
- Manufacturing: Tata Motors, Mahindra, Bajaj Auto, BHEL
- Finance: HDFC Bank, ICICI Bank, SBI, JPMorgan Chase
- Media: Times of India, Hindustan Times, NDTV
- E-commerce: Flipkart, Zomato, Swiggy, BigBasket

## 🏆 Hackathon-Ready Features

### Technical Excellence

- ✅ Full-stack implementation (Frontend + Backend + AI)
- ✅ RESTful API design
- ✅ Machine learning integration
- ✅ Responsive UI/UX
- ✅ Error handling & validation

### Business Impact

- ✅ Real-world problem solving (PM Internship Scheme)
- ✅ Government initiative alignment
- ✅ Scalable architecture
- ✅ Industry partnerships potential

### Innovation

- ✅ Dynamic skill matching by education field
- ✅ Multi-criteria recommendation algorithm
- ✅ Real company integration
- ✅ Government portal connectivity

## 🔧 API Endpoints

### Health Check

```
GET /health
Response: {"status": "healthy", "timestamp": "..."}
```

### Get Recommendations

```
POST /api/recommendations
Content-Type: application/json

Body:
{
  "education": "Computer Science",
  "skills": ["Python", "Web Development"],
  "location_preference": "bangalore",
  "min_stipend": 20000
}

Response:
{
  "success": true,
  "recommendations": [...],
  "count": 10
}
```

## 🎨 UI/UX Highlights

- Government branding with orange/saffron color scheme
- Interactive skill tags with hover effects
- Real-time form validation
- Loading animations and success notifications
- Mobile-responsive design
- Professional card layouts for recommendations

## 🚀 Future Enhancements

- [ ] User authentication system
- [ ] Save/bookmark internships
- [ ] Application tracking dashboard
- [ ] Company profile pages
- [ ] Advanced filters (duration, start date)
- [ ] Email notifications
- [ ] Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

Shreyas Raut (@Om Raj Singh)

- 🎓 Passionate about connecting students with opportunities
- 🏛️ Supporting Government of India's PM Internship Scheme
- 🚀 Building technology for social impact

## 🙏 Acknowledgments

- Government of India - PM Internship Scheme initiative
- Ministry of Corporate Affairs - Official program support
- Indian IT Industry - Partnership and opportunities
- Open Source Community - Tools and frameworks

---    

## 🇮🇳 Supporting Digital India Initiative

This project aligns with the Government of India's vision of empowering youth through technology and creating employment opportunities for the digital age.

Built with ❤️ for India's future workforce

---

🏆 Ready to change the future of internships in India! 🚀
