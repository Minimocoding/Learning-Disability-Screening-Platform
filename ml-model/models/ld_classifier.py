import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

class LearningDifferenceClassifier:
    """
    ML model for classifying learning differences based on screening questionnaire responses.
    This is a basic implementation that can be enhanced with real clinical data.
    """
    
    def __init__(self):
        self.ld_classifier = None  # Binary classifier for LD detection
        self.type_classifier = None  # Multi-class classifier for LD type
        self.mental_health_classifier = None  # Binary classifier for mental health flag
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=1000):
        """
        Generate synthetic training data for demonstration purposes.
        In production, this would be replaced with real clinical data.
        """
        np.random.seed(42)
        
        # Generate 50 questionnaire responses (0-2 scale)
        X = np.random.randint(0, 3, size=(n_samples, 50))
        
        # Create synthetic labels based on patterns
        ld_labels = []
        type_labels = []
        mental_health_labels = []
        
        for i in range(n_samples):
            responses = X[i]
            total_score = np.sum(responses)
            
            # LD classification based on total score and patterns
            has_ld = total_score > 35 or np.sum(responses == 2) > 15
            ld_labels.append(1 if has_ld else 0)
            
            if has_ld:
                # Type classification based on question groups
                dyslexia_score = np.sum(responses[0::3])  # Every 3rd question starting from 0
                dyscalculia_score = np.sum(responses[1::3])  # Every 3rd question starting from 1
                dysgraphia_score = np.sum(responses[2::3])  # Every 3rd question starting from 2
                
                scores = [dyslexia_score, dyscalculia_score, dysgraphia_score]
                primary_type = np.argmax(scores)  # 0=dyslexia, 1=dyscalculia, 2=dysgraphia
                type_labels.append(primary_type)
                
                # Mental health flag based on high stress indicators
                mental_health_flag = total_score > 70 or np.sum(responses == 2) > 25
                mental_health_labels.append(1 if mental_health_flag else 0)
            else:
                type_labels.append(-1)  # No LD type
                mental_health_labels.append(0)
        
        return X, np.array(ld_labels), np.array(type_labels), np.array(mental_health_labels)
    
    def extract_features(self, responses):
        """
        Extract meaningful features from raw questionnaire responses.
        """
        responses = np.array(responses)
        
        features = []
        
        # Basic statistics
        features.extend([
            np.sum(responses),  # Total score
            np.mean(responses),  # Average response
            np.std(responses),  # Response variability
            np.sum(responses == 0),  # Count of "No" responses
            np.sum(responses == 1),  # Count of "Sometimes" responses
            np.sum(responses == 2),  # Count of "Yes" responses
        ])
        
        # Category-specific scores (assuming questions are grouped by category)
        dyslexia_questions = responses[0::3]  # Every 3rd starting from 0
        dyscalculia_questions = responses[1::3]  # Every 3rd starting from 1
        dysgraphia_questions = responses[2::3]  # Every 3rd starting from 2
        
        features.extend([
            np.sum(dyslexia_questions),
            np.mean(dyslexia_questions),
            np.sum(dyscalculia_questions),
            np.mean(dyscalculia_questions),
            np.sum(dysgraphia_questions),
            np.mean(dysgraphia_questions),
        ])
        
        # Pattern-based features
        features.extend([
            len([i for i in range(len(responses)-1) if responses[i] == 2 and responses[i+1] == 2]),  # Consecutive high scores
            np.max([np.sum(responses[i:i+5]) for i in range(len(responses)-4)]),  # Max score in any 5-question window
        ])
        
        # Add the original responses as features too
        features.extend(responses)
        
        return np.array(features)
    
    def train(self, training_data=None):
        """
        Train the ML models on the provided data.
        """
        if training_data is None:
            # Generate synthetic data for demonstration
            print("Generating synthetic training data...")
            X_raw, y_ld, y_type, y_mental = self.generate_synthetic_data()
        else:
            X_raw, y_ld, y_type, y_mental = training_data
        
        # Extract features from raw responses
        print("Extracting features...")
        X_features = np.array([self.extract_features(responses) for responses in X_raw])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X_features)
        
        # Train LD detection model
        print("Training LD detection model...")
        self.ld_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.ld_classifier.fit(X_scaled, y_ld)
        
        # Train LD type classification model (only on positive LD cases)
        ld_positive_mask = y_ld == 1
        if np.sum(ld_positive_mask) > 10:  # Ensure we have enough positive cases
            print("Training LD type classification model...")
            X_ld_positive = X_scaled[ld_positive_mask]
            y_type_positive = y_type[ld_positive_mask]
            
            self.type_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            self.type_classifier.fit(X_ld_positive, y_type_positive)
        
        # Train mental health flag model
        print("Training mental health screening model...")
        self.mental_health_classifier = LogisticRegression(random_state=42)
        self.mental_health_classifier.fit(X_scaled, y_mental)
        
        self.is_trained = True
        print("Training completed successfully!")
        
        # Evaluate models
        self._evaluate_models(X_scaled, y_ld, y_type, y_mental)
    
    def _evaluate_models(self, X, y_ld, y_type, y_mental):
        """
        Evaluate the trained models and print performance metrics.
        """
        print("\n=== Model Evaluation ===")
        
        # LD Detection Model
        ld_scores = cross_val_score(self.ld_classifier, X, y_ld, cv=5)
        print(f"LD Detection Accuracy: {np.mean(ld_scores):.3f} (+/- {np.std(ld_scores) * 2:.3f})")
        
        # Type Classification Model
        if self.type_classifier is not None:
            ld_positive_mask = y_ld == 1
            if np.sum(ld_positive_mask) > 5:
                X_ld_positive = X[ld_positive_mask]
                y_type_positive = y_type[ld_positive_mask]
                type_scores = cross_val_score(self.type_classifier, X_ld_positive, y_type_positive, cv=3)
                print(f"LD Type Classification Accuracy: {np.mean(type_scores):.3f} (+/- {np.std(type_scores) * 2:.3f})")
        
        # Mental Health Model
        mh_scores = cross_val_score(self.mental_health_classifier, X, y_mental, cv=5)
        print(f"Mental Health Screening Accuracy: {np.mean(mh_scores):.3f} (+/- {np.std(mh_scores) * 2:.3f})")
    
    def predict(self, responses):
        """
        Make predictions for a single set of questionnaire responses.
        
        Args:
            responses: List or array of 50 responses (values 0-2)
            
        Returns:
            dict: Prediction results including LD status, type, and mental health flag
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Extract features and scale
        features = self.extract_features(responses).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Predict LD status
        ld_prob = self.ld_classifier.predict_proba(features_scaled)[0]
        has_ld = self.ld_classifier.predict(features_scaled)[0]
        ld_confidence = max(ld_prob)
        
        # Predict LD type if LD is detected
        primary_type = None
        type_confidence = 0.0
        if has_ld and self.type_classifier is not None:
            type_probs = self.type_classifier.predict_proba(features_scaled)[0]
            type_pred = self.type_classifier.predict(features_scaled)[0]
            primary_type = ['dyslexia', 'dyscalculia', 'dysgraphia'][type_pred]
            type_confidence = max(type_probs)
        
        # Predict mental health flag
        mh_prob = self.mental_health_classifier.predict_proba(features_scaled)[0]
        mental_health_flag = self.mental_health_classifier.predict(features_scaled)[0]
        mh_confidence = max(mh_prob)
        
        # Calculate category scores
        responses = np.array(responses)
        category_scores = {
            'dyslexia': np.sum(responses[0::3]),
            'dyscalculia': np.sum(responses[1::3]),
            'dysgraphia': np.sum(responses[2::3])
        }
        
        return {
            'hasLearningDifference': bool(has_ld),
            'primaryType': primary_type,
            'categoryScores': category_scores,
            'totalScore': int(np.sum(responses)),
            'mentalHealthFlag': bool(mental_health_flag),
            'confidence': float(ld_confidence),
            'typeConfidence': float(type_confidence),
            'mentalHealthConfidence': float(mh_confidence)
        }
    
    def save_model(self, filepath):
        """
        Save the trained model to disk.
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'ld_classifier': self.ld_classifier,
            'type_classifier': self.type_classifier,
            'mental_health_classifier': self.mental_health_classifier,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model from disk.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.ld_classifier = model_data['ld_classifier']
        self.type_classifier = model_data['type_classifier']
        self.mental_health_classifier = model_data['mental_health_classifier']
        self.scaler = model_data['scaler']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {filepath}")

# Example usage and training
if __name__ == "__main__":
    # Create and train the model
    classifier = LearningDifferenceClassifier()
    classifier.train()
    
    # Save the model
    os.makedirs('../models', exist_ok=True)
    classifier.save_model('../models/ld_classifier.joblib')
    
    # Test with sample responses
    sample_responses = [1, 2, 0, 1, 1, 2, 0, 1, 2, 1,
                       0, 1, 2, 1, 0, 2, 1, 0, 1, 2,
                       1, 0, 2, 1, 0, 1, 2, 0, 1, 1,
                       2, 1, 0, 1, 2, 0, 1, 2, 1, 0,
                       1, 2, 0, 1, 1, 2, 0, 1, 2, 1]
    
    result = classifier.predict(sample_responses)
    print("\n=== Sample Prediction ===")
    print(f"Has LD: {result['hasLearningDifference']}")
    print(f"Primary Type: {result['primaryType']}")
    print(f"Category Scores: {result['categoryScores']}")
    print(f"Total Score: {result['totalScore']}")
    print(f"Mental Health Flag: {result['mentalHealthFlag']}")
    print(f"Confidence: {result['confidence']:.3f}")