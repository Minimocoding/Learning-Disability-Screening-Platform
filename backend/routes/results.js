const express = require('express');
const { authenticateToken } = require('../middleware/auth');
const TestResult = require('../models/TestResult');
const router = express.Router();

// @route   GET /api/results
// @desc    Get all test results for the authenticated user
// @access  Private
router.get('/', authenticateToken, async (req, res) => {
    try {
        const results = await TestResult.find({ userId: req.user.userId })
            .populate('userId', 'userName childInfo')
            .sort({ submittedAt: -1 });

        res.json({
            message: 'Results retrieved successfully',
            results,
            total: results.length
        });
    } catch (error) {
        console.error('Error fetching results:', error);
        res.status(500).json({ error: 'Failed to fetch results' });
    }
});

// @route   GET /api/results/:id
// @desc    Get specific test result
// @access  Private
router.get('/:id', authenticateToken, async (req, res) => {
    try {
        const result = await TestResult.findOne({
            _id: req.params.id,
            userId: req.user.userId
        }).populate('userId', 'userName childInfo');

        if (!result) {
            return res.status(404).json({ error: 'Result not found' });
        }

        res.json({
            message: 'Result retrieved successfully',
            result
        });
    } catch (error) {
        console.error('Error fetching result:', error);
        res.status(500).json({ error: 'Failed to fetch result' });
    }
});

// @route   DELETE /api/results/:id
// @desc    Delete a test result
// @access  Private
router.delete('/:id', authenticateToken, async (req, res) => {
    try {
        const result = await TestResult.findOneAndDelete({
            _id: req.params.id,
            userId: req.user.userId
        });

        if (!result) {
            return res.status(404).json({ error: 'Result not found' });
        }

        res.json({
            message: 'Result deleted successfully'
        });
    } catch (error) {
        console.error('Error deleting result:', error);
        res.status(500).json({ error: 'Failed to delete result' });
    }
});

module.exports = router;