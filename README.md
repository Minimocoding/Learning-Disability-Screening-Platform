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
# Learning Helper - Interactive Django Website

A comprehensive interactive Django website for screening learning disabilities in children. The application provides early identification and assessment tools for dyslexia, dyscalculia, dysgraphia, and psychological impact.

## Features

### 🏠 Homepage
- Beautiful, child-friendly design inspired by the reference image
- Clear navigation and call-to-action buttons
- Responsive design with Bootstrap 5
- Animated elements and modern UI

### 👥 Multi-User Registration System
- **Parents/Guardians**: Register as father, mother, sibling, or other family member
- **Teachers/Educators**: Professional registration with school information
- **Psychologists**: Professional registration with qualifications and organization details
- Secure authentication system with username/email login

### 📋 Learning Disability Assessment
- **50 Comprehensive Questions** divided into 4 categories:
  - Questions 1-11: Dyslexia indicators
  - Questions 12-22: Dysgraphia indicators  
  - Questions 23-35: Dyscalculia indicators
  - Questions 36-50: Psychological impact assessment

### 🎯 Smart Assessment Features
- Progressive section-based questionnaire
- Real-time progress tracking
- Interactive answer selection (Yes/Sometimes/No)
- Form validation and completion tracking
- Child information collection before assessment

### 📊 Intelligent Results System
- **Threshold-based scoring algorithm**:
  - Dyslexia threshold: 12/22 points
  - Dysgraphia threshold: 12/22 points  
  - Dyscalculia threshold: 15/26 points
  - Psychological impact threshold: 18/30 points
  - Overall LD threshold: 35/100 points

- **Progressive results display with 2-second delays**:
  1. Overall learning disability assessment
  2. Specific LD type breakdown (if applicable)
  3. Psychological impact evaluation
  4. Detailed recommendations and next steps

### 🎨 Modern UI/UX
- Gradient backgrounds and animations
- Custom CSS variables for consistent theming
- Card-based layouts with hover effects
- Loading spinners and smooth transitions
- Mobile-responsive design

## Technical Specifications

### Backend
- **Framework**: Django 5.2.6
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django's built-in auth system
- **Models**: User profiles, child information, test questions, and results
- **Admin Interface**: Full admin panel for managing questions and results

### Frontend
- **CSS Framework**: Bootstrap 5.1.3
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JS for interactivity
- **Animations**: CSS transitions and keyframe animations
- **Responsive**: Mobile-first design approach

### Database Schema
- **UserProfile**: Links to Django User with user type
- **ParentProfile**: Additional parent-specific information
- **TeacherProfile**: School information
- **PsychologistProfile**: Professional credentials
- **Child**: Child information for assessment
- **TestQuestion**: 50 predefined assessment questions
- **TestResult**: Complete assessment results with scoring

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2.6
- Virtual environment (recommended)

### Quick Start
```bash
# Clone the repository
cd learning-helper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install django

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Populate test questions
python manage.py populate_questions

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Usage Flow

### 1. Registration
1. Visit the homepage
2. Click "Get Started" or "Register"
3. Choose user type (Parent, Teacher, or Psychologist)
4. Fill out the registration form
5. Account automatically created and logged in

### 2. Taking Assessment
1. Navigate to "Take Test" (requires login)
2. Read assessment guidelines
3. Enter child information
4. Answer 50 questions across 4 sections
5. Submit for results

### 3. Viewing Results
1. Results displayed progressively with 2-second delays
2. Overall LD assessment shown first
3. Specific LD breakdowns (if applicable)
4. Psychological impact assessment
5. Recommendations and next steps

## Assessment Algorithm

### Scoring System
- **Yes**: 2 points
- **Sometimes**: 1 point  
- **No**: 0 points

### Prediction Logic
```python
# Individual LD thresholds
DYSLEXIA_THRESHOLD = 12  # out of 22
DYSGRAPHIA_THRESHOLD = 12  # out of 22  
DYSCALCULIA_THRESHOLD = 15  # out of 26
PSYCHOLOGICAL_THRESHOLD = 18  # out of 30

# Overall LD threshold
TOTAL_LD_THRESHOLD = 35  # out of 100

# Child has LD if:
has_ld = total_score >= 35 OR any_individual_ld_detected
```

## File Structure
```
learning-helper/
├── learning_helper/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── main/                     # Main application
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── populate_questions.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/                # HTML templates
│   ├── base.html
│   └── main/
│       ├── home.html
│       ├── about_ld.html
│       ├── register_*.html
│       ├── login.html
│       ├── take_test.html
│       ├── test_guidelines.html
│       ├── child_info.html
│       ├── test_questions.html
│       └── test_results.html
├── static/                   # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
├── manage.py
└── README.md
```

## Admin Interface

Access the admin panel at `/admin/` with superuser credentials:
- Manage test questions
- View test results and analytics
- Monitor user registrations
- Export data for research

## Security Features

- CSRF protection on all forms
- User authentication required for assessments
- Session-based child information storage
- Secure password hashing
- SQL injection protection via Django ORM

## Customization

### Adding New Questions
1. Access Django admin panel
2. Navigate to "Test Questions"
3. Add questions with appropriate categories
4. Questions automatically appear in assessment

### Modifying Thresholds
Edit threshold values in `models.py`:
```python
def predict_ld(self):
    DYSLEXIA_THRESHOLD = 12  # Adjust as needed
    # ... other thresholds
```

## Future Enhancements

- [ ] Multi-language support
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Integration with school systems
- [ ] Professional consultation booking

## Support & Documentation

- **Demo**: Available at development server
- **Admin Panel**: Full CRUD operations
- **Database**: Easily exportable for analysis
- **Responsive**: Works on all devices

## License

This project is created for educational and assessment purposes. Please consult with licensed professionals for official diagnoses.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

---

**Note**: This screening tool is for educational purposes and should not replace professional psychological evaluation. Always consult qualified professionals for comprehensive assessment and diagnosis.
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

- **Email**: Contributors :Hemangi Kayarkar 
                           Gouri Bijwe 
                           Ayush Atkari 
                           Arsh Tarare 
- **Documentation**: [docs.learninghelper.com](https://docs.learninghelper.com)
- **Issues**: GitHub Issues tab
- **Discussions**: GitHub Discussions

---

**Made with ❤️ for helping children learn better**

*Learning Helper Team - Empowering every child's unique learning journey*
