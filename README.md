# 🌟 Learning Helper

**A comprehensive, child-friendly website for learning difference screening**

Learning Helper is a full-stack web application designed to help parents, teachers, and psychologists screen children for learning differences such as Dyslexia, Dyscalculia, and Dysgraphia. The platform combines a colorful, engaging user interface with machine learning-powered assessment tools.

## ✨ Features

### 🎯 Core Functionality
- **Interactive 50-Question Screening Test**: Child-friendly interface with emoji-based responses
- **Multi-User Support**: Designed for parents, teachers, and psychologists
- **Intelligent Assessment**: ML-powered classification for learning difference detection
- **Comprehensive Results**: Detailed analysis with type classification and recommendations
- **Mental Health Screening**: Basic emotional well-being indicators

### 🎨 User Experience
- **Child-Friendly Design**: Colorful, animated interface with engaging visuals
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Accessibility**: High contrast colors and readable fonts
- **Interactive Elements**: Smooth animations and hover effects

### 📊 Assessment Features
- **Real-time Scoring**: Dynamic progress tracking during assessment
- **Category Breakdown**: Separate scoring for Dyslexia, Dyscalculia, and Dysgraphia
- **Confidence Indicators**: ML model confidence levels for results
- **Professional Recommendations**: Tailored next-step guidance

## 🏗️ Project Structure

```
learning-helper/
├── frontend/                 # React-style vanilla JS frontend
│   ├── index.html           # Main landing page
│   ├── results.html         # Results display page
│   ├── css/
│   │   ├── style.css        # Main styles with animations
│   │   └── results.css      # Results page specific styles
│   ├── js/
│   │   ├── main.js          # Main functionality and test logic
│   │   └── results.js       # Results page JavaScript
│   └── images/              # Logo and visual assets
├── backend/                 # Node.js/Express API server
│   ├── server.js           # Main server file
│   ├── package.json        # Dependencies and scripts
│   ├── routes/             # API route handlers
│   │   ├── auth.js         # Authentication routes
│   │   ├── users.js        # User management
│   │   ├── test.js         # Test and assessment routes
│   │   └── results.js      # Results management
│   ├── models/             # MongoDB data models
│   │   ├── User.js         # User schema
│   │   ├── Question.js     # Test questions schema
│   │   └── TestResult.js   # Results storage schema
│   ├── middleware/         # Custom middleware
│   │   └── auth.js         # JWT authentication
│   └── controllers/        # Business logic (planned)
├── ml-model/               # Machine Learning components
│   ├── api_server.py       # Flask API for ML inference
│   ├── requirements.txt    # Python dependencies
│   ├── models/
│   │   └── ld_classifier.py # Scikit-learn based classifier
│   └── data/               # Training data (planned)
├── database/               # Database configurations
│   └── schema.sql          # Database schema (planned)
├── docs/                   # Additional documentation
└── README.md               # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- **Node.js** (v16+ recommended)
- **Python** (v3.8+ for ML components)
- **MongoDB** (local or cloud instance)
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/learning-helper.git
   cd learning-helper
   ```

2. **Set up Backend**
   ```bash
   cd backend
   npm install
   
   # Create environment file
   echo "JWT_SECRET=your-super-secret-key
   MONGODB_URI=mongodb://localhost:27017/learning-helper
   PORT=5000
   NODE_ENV=development" > .env
   ```

3. **Set up ML Model**
   ```bash
   cd ../ml-model
   pip install -r requirements.txt
   
   # Train and save the initial model
   python models/ld_classifier.py
   ```

4. **Start the Services**
   
   **Terminal 1 - Backend API:**
   ```bash
   cd backend
   npm run dev
   ```
   
   **Terminal 2 - ML API:**
   ```bash
   cd ml-model
   python api_server.py
   ```
   
   **Terminal 3 - Frontend (Simple HTTP Server):**
   ```bash
   cd frontend
   # Python 3
   python -m http.server 3000
   # Or with Node.js
   npx serve -p 3000
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - ML API: http://localhost:5001

## 🎮 Usage Guide

### For Parents/Guardians

1. **Register**: Create an account with your user type (parent/teacher/psychologist)
2. **Child Information**: Provide your child's details (name, age, school, grade)
3. **Take Assessment**: Complete the 50-question screening test
4. **View Results**: Get detailed analysis with recommendations
5. **Share Results**: Generate links to share with professionals

### For Educators/Psychologists

1. **Professional Registration**: Register with educator or psychologist role
2. **Multiple Assessments**: Manage assessments for different children
3. **Result Analysis**: Access detailed breakdowns and confidence metrics
4. **Recommendations**: Get tailored next-step guidance

## 🧠 ML Model Details

### Classification Approach
- **Binary Classification**: Learning Difference detection (Yes/No)
- **Multi-class Classification**: Type classification (Dyslexia/Dyscalculia/Dysgraphia)
- **Mental Health Screening**: Basic emotional indicator flagging

### Features Extracted
- Total assessment score
- Category-specific scores
- Response patterns and consistency
- Consecutive high-concern indicators
- Statistical measures (mean, std, etc.)

### Model Performance
- **Cross-validation Accuracy**: ~85% (synthetic data)
- **Confidence Calibration**: Probability estimates for uncertainty
- **Interpretability**: Feature importance and category breakdown

> **Note**: Current model uses synthetic data for demonstration. Production deployment requires clinical validation with real assessment data.

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
# Database
MONGODB_URI=mongodb://localhost:27017/learning-helper

# Authentication
JWT_SECRET=your-super-secret-jwt-key-here

# Server
PORT=5000
NODE_ENV=development
FRONTEND_URL=http://localhost:3000

# ML Integration
ML_API_URL=http://localhost:5001
```

**ML API**
```env
# Flask Configuration
ML_API_PORT=5001
FLASK_DEBUG=true

# Model Settings
MODEL_PATH=models/ld_classifier.joblib
```

## 📡 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/verify` - Token verification

### Assessment Endpoints
- `GET /api/test/questions` - Fetch test questions
- `POST /api/test/submit` - Submit test responses
- `GET /api/test/results/:id` - Get specific result

### User Management
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile

### Results Management
- `GET /api/results` - Get user's results history
- `DELETE /api/results/:id` - Delete a result

## 🎨 Design System

### Color Palette
- **Primary**: `#ff6b6b` (Coral)
- **Secondary**: `#4ecdc4` (Turquoise) 
- **Accent**: `#ffa500` (Orange)
- **Success**: `#00b894` (Green)
- **Warning**: `#fdcb6e` (Yellow)

### Typography
- **Primary Font**: 'Comic Neue' (child-friendly)
- **Fallback**: Cursive, sans-serif

### Animations
- **Bounce effects** for interactive elements
- **Smooth transitions** (0.3s ease)
- **Loading spinners** with CSS animations
- **Progress bars** with smooth fills

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd backend
npm test

# ML Model validation
cd ml-model
python -m pytest tests/
```

### Test Coverage
- API endpoint testing
- Authentication flow validation
- ML model accuracy testing
- Frontend interaction testing

## 🚀 Deployment

### Production Checklist
- [ ] Set strong JWT secrets
- [ ] Configure production database
- [ ] Set up SSL certificates
- [ ] Configure environment variables
- [ ] Set up monitoring and logging
- [ ] Train model with real clinical data
- [ ] Implement proper error tracking

### Docker Deployment (Planned)
```bash
docker-compose up -d
```

## 🤝 Contributing

We welcome contributions! Please read our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Use consistent code formatting
- Add comments for complex logic
- Include tests for new features
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Disclaimers

### Clinical Use
- This tool is for **screening purposes only**
- **Not a substitute** for professional diagnosis
- Results should be **interpreted by qualified professionals**
- Always consult healthcare providers for comprehensive assessment

### Data Privacy
- User data is encrypted and stored securely
- No personal information is shared without consent
- Comply with local privacy regulations (GDPR, COPPA, etc.)

## 🎯 Future Enhancements

### Planned Features
- [ ] **Advanced ML Models**: Deep learning integration
- [ ] **Multi-language Support**: Internationalization
- [ ] **Professional Dashboard**: Enhanced tools for educators
- [ ] **Progress Tracking**: Longitudinal assessment history
- [ ] **Integration APIs**: Connect with school systems
- [ ] **Mobile App**: Native iOS/Android applications

### Research Opportunities
- Clinical validation studies
- Longitudinal outcome tracking
- Cross-cultural assessment adaptation
- Integration with educational interventions

## 📞 Support

For support, questions, or collaboration opportunities:

- **Email**: support@learninghelper.com
- **Documentation**: [docs.learninghelper.com](https://docs.learninghelper.com)
- **Issues**: GitHub Issues tab
- **Discussions**: GitHub Discussions

---

**Made with ❤️ for helping children learn better**

*Learning Helper Team - Empowering every child's unique learning journey*