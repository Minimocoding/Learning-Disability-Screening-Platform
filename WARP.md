# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Architecture Overview

Learning Helper is a **three-tier full-stack application** for screening learning differences in children:

1. **Frontend**: Vanilla JavaScript SPA with child-friendly UI (serves on port 3000)
2. **Backend**: Node.js/Express REST API with MongoDB (serves on port 5000)
3. **ML Model**: Python Flask API with scikit-learn classifier (serves on port 5001)

### Key Architectural Patterns
- **Microservices approach**: Separate ML inference service from main backend
- **JWT-based authentication**: User sessions managed with tokens
- **MongoDB document structure**: Users embed child information, results stored separately
- **Feature extraction pipeline**: Raw questionnaire responses → engineered features → ML prediction
- **Synthetic data training**: Current ML model uses generated data (placeholder for real clinical data)

## Development Commands

### Backend (Node.js/Express)
```bash
# Install dependencies and start development server
cd backend
npm install
npm run dev          # Start with nodemon for hot reload

# Other commands
npm start           # Production start
npm test           # Run Jest tests
```

### ML Model (Python Flask)
```bash
# Setup and start ML API
cd ml-model
pip install -r requirements.txt
python models/ld_classifier.py    # Train and save initial model
python api_server.py              # Start Flask ML API server
```

### Frontend (Static Files)
```bash
# Serve frontend (choose one method)
cd frontend
python -m http.server 3000        # Python HTTP server
# OR
npx serve -p 3000                 # Node.js serve
```

### Database Setup
Ensure MongoDB is running locally or set `MONGODB_URI` in backend/.env

## Critical Data Flow

### Assessment Process
1. **User Registration**: Frontend → `/api/auth/register` → MongoDB User collection
2. **Authentication**: Login → JWT token → Stored in frontend localStorage
3. **Test Submission**: 50 answers → `/api/test/submit` → ML API → Results storage
4. **ML Inference**: Answers → Feature extraction → RandomForest classifier → Confidence scores

### ML Model Architecture
- **Binary classifier**: Learning Difference detection (RandomForest)
- **Multi-class classifier**: LD type classification (RandomForest) 
- **Mental health flagging**: Basic emotional indicators (LogisticRegression)
- **Feature engineering**: Category scores, patterns, statistical measures from 50 responses

## Environment Configuration

### Backend (.env required)
```env
JWT_SECRET=your-super-secret-jwt-key-here
MONGODB_URI=mongodb://localhost:27017/learning-helper
PORT=5000
NODE_ENV=development
FRONTEND_URL=http://localhost:3000
ML_API_URL=http://localhost:5001
```

### ML API Configuration
- Model auto-trains on startup if no saved model exists
- Saved models stored in `ml-model/models/ld_classifier.joblib`
- Uses synthetic data generation for demonstration

## Key Business Logic

### Question Categories (Every 3rd Pattern)
- **Dyslexia indicators**: Questions 0, 3, 6, 9... (reading/language)
- **Dyscalculia indicators**: Questions 1, 4, 7, 10... (math/numbers)  
- **Dysgraphia indicators**: Questions 2, 5, 8, 11... (writing/motor)

### Scoring Thresholds
- **LD Detection**: Total score ≥ 35 (out of 100 max)
- **Mental Health Flag**: High consecutive scores (pattern "2222") OR total > 75
- **Confidence Calculation**: ML model probability estimates

## Database Schema

### User Model (MongoDB)
- Embeds child information (name, age, school, grade)
- Supports three user types: parent, teacher, psychologist
- JWT authentication with bcryptjs password hashing

### Test Results Storage
- Links to User via ObjectId
- Stores raw answers array [50 integers 0-2]
- Stores ML prediction results with confidence scores

## Testing Strategy

### Backend Testing
```bash
cd backend
npm test  # Jest test suite for API endpoints and models
```

### ML Model Testing
Current model uses cross-validation on synthetic data. For production:
- Requires clinical validation with real assessment data
- Need A/B testing framework for model performance
- Longitudinal outcome tracking for effectiveness

## Production Deployment Notes

### Critical Security Requirements
- Strong JWT secrets in production
- HTTPS/SSL certificates required
- Rate limiting already configured (100 requests/15 minutes)
- Input validation with express-validator

### ML Model Production Considerations
- Current model is demonstration-only with synthetic data
- Requires clinical data validation before real deployment
- Need model versioning and rollback capabilities
- Consider moving to more robust ML infrastructure (e.g., TensorFlow Serving)

### Performance Considerations
- Frontend uses vanilla JS (no build process needed)
- Backend uses MongoDB connection pooling
- ML API loads model once on startup (memory-based inference)

## Development Workflow

When making changes to the assessment flow:
1. **Update questions**: Modify backend/models/Question.js schema and seed data
2. **Adjust ML features**: Update feature extraction in ml-model/models/ld_classifier.py
3. **Frontend updates**: Sync question rendering in frontend/js/main.js
4. **Retrain model**: Use `/retrain` endpoint or restart ML API

When adding new user types or roles:
1. Update User model enum in backend/models/User.js
2. Modify registration flow in frontend and backend/routes/auth.js
3. Consider permission-based access in middleware/auth.js