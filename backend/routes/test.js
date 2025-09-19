const express = require('express');
const { body, validationResult } = require('express-validator');
const Question = require('../models/Question');
const TestResult = require('../models/TestResult');
const { authenticateToken } = require('../middleware/auth');
const router = express.Router();

// @route   GET /api/test/questions
// @desc    Get all test questions
// @access  Private
router.get('/questions', authenticateToken, async (req, res) => {
    try {
        const questions = await Question.find({ active: true })
            .select('-correctAnswer -category') // Don't expose internal fields
            .sort({ questionNumber: 1 });

        res.json({
            message: 'Questions retrieved successfully',
            questions,
            total: questions.length
        });
    } catch (error) {
        console.error('Error fetching questions:', error);
        res.status(500).json({ error: 'Failed to fetch questions' });
    }
});

// @route   POST /api/test/submit
// @desc    Submit test answers and get results
// @access  Private
router.post('/submit', [
    authenticateToken,
    body('answers').isArray({ min: 50, max: 50 }).withMessage('Must provide exactly 50 answers'),
    body('answers.*').isInt({ min: 0, max: 2 }).withMessage('Each answer must be 0, 1, or 2')
], async (req, res) => {
    try {
        // Check for validation errors
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ 
                error: 'Validation failed', 
                details: errors.array() 
            });
        }

        const { answers } = req.body;
        const userId = req.user.userId;

        // Calculate basic scores
        const totalScore = answers.reduce((sum, answer) => sum + answer, 0);
        
        // Get questions to calculate category scores
        const questions = await Question.find({ active: true }).sort({ questionNumber: 1 });
        
        const categoryScores = {
            dyslexia: 0,
            dyscalculia: 0,
            dysgraphia: 0
        };

        // Calculate category scores
        questions.forEach((question, index) => {
            if (index < answers.length && categoryScores.hasOwnProperty(question.category)) {
                categoryScores[question.category] += answers[index];
            }
        });

        // Simple ML-like classification (placeholder for real ML model)
        const hasLD = totalScore >= 35; // Threshold for LD detection
        
        // Determine primary type based on highest category score
        const sortedCategories = Object.entries(categoryScores)
            .sort(([,a], [,b]) => b - a);
        const primaryType = hasLD ? sortedCategories[0][0] : null;

        // Simple mental health indicator (placeholder logic)
        const highScoreStreak = answers.join('').includes('2222'); // Four consecutive high scores
        const mentalHealthFlag = hasLD && (totalScore > 75 || highScoreStreak);

        // Create assessment result
        const result = {
            hasLearningDifference: hasLD,
            primaryType: primaryType,
            categoryScores: categoryScores,
            totalScore: totalScore,
            mentalHealthFlag: mentalHealthFlag,
            confidence: hasLD ? Math.min(0.95, (totalScore / 100) + 0.5) : Math.max(0.1, 1 - (totalScore / 100))
        };

        // Save test result to database
        const testResult = new TestResult({
            userId: userId,
            answers: answers,
            results: result,
            submittedAt: new Date()
        });

        await testResult.save();

        res.json({
            message: 'Test submitted successfully',
            testId: testResult._id,
            results: result,
            recommendations: generateRecommendations(result)
        });

    } catch (error) {
        console.error('Error submitting test:', error);
        res.status(500).json({ error: 'Failed to submit test' });
    }
});

// @route   GET /api/test/results/:testId
// @desc    Get specific test results
// @access  Private
router.get('/results/:testId', authenticateToken, async (req, res) => {
    try {
        const { testId } = req.params;
        const userId = req.user.userId;

        const testResult = await TestResult.findOne({ 
            _id: testId, 
            userId: userId 
        }).populate('userId', 'userName childInfo');

        if (!testResult) {
            return res.status(404).json({ error: 'Test result not found' });
        }

        res.json({
            message: 'Test results retrieved successfully',
            result: testResult,
            recommendations: generateRecommendations(testResult.results)
        });

    } catch (error) {
        console.error('Error fetching test results:', error);
        res.status(500).json({ error: 'Failed to fetch test results' });
    }
});

// Helper function to generate recommendations based on results
function generateRecommendations(results) {
    const recommendations = [];

    if (results.hasLearningDifference) {
        recommendations.push({
            type: 'professional',
            message: 'Consult with a qualified educational psychologist for a comprehensive evaluation.'
        });

        if (results.primaryType === 'dyslexia') {
            recommendations.push({
                type: 'educational',
                message: 'Consider structured literacy programs and multisensory reading approaches.'
            });
        } else if (results.primaryType === 'dyscalculia') {
            recommendations.push({
                type: 'educational',
                message: 'Explore visual-spatial approaches to mathematics and concrete manipulatives.'
            });
        } else if (results.primaryType === 'dysgraphia') {
            recommendations.push({
                type: 'educational',
                message: 'Consider assistive technology for writing and occupational therapy evaluation.'
            });
        }

        if (results.mentalHealthFlag) {
            recommendations.push({
                type: 'support',
                message: 'Consider counseling support to address potential emotional impacts of learning challenges.'
            });
        }
    } else {
        recommendations.push({
            type: 'general',
            message: 'Results suggest typical development. Continue supporting your child\'s learning journey.'
        });
    }

    recommendations.push({
        type: 'disclaimer',
        message: 'This screening is not a diagnosis. Always consult qualified professionals for comprehensive assessment.'
    });

    return recommendations;
}

module.exports = router;