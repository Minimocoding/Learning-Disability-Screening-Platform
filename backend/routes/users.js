const express = require('express');
const { authenticateToken } = require('../middleware/auth');
const User = require('../models/User');
const router = express.Router();

// @route   GET /api/users/profile
// @desc    Get user profile
// @access  Private
router.get('/profile', authenticateToken, async (req, res) => {
    try {
        const user = await User.findById(req.user.userId).select('-password');
        
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({
            message: 'Profile retrieved successfully',
            user: {
                id: user._id,
                userName: user.userName,
                email: user.email,
                phone: user.phone,
                userType: user.userType,
                childInfo: user.childInfo,
                createdAt: user.createdAt
            }
        });
    } catch (error) {
        console.error('Error fetching user profile:', error);
        res.status(500).json({ error: 'Failed to fetch profile' });
    }
});

// @route   PUT /api/users/profile
// @desc    Update user profile
// @access  Private
router.put('/profile', authenticateToken, async (req, res) => {
    try {
        const { userName, phone, childInfo } = req.body;
        
        const updateFields = {};
        if (userName) updateFields.userName = userName;
        if (phone) updateFields.phone = phone;
        if (childInfo) updateFields.childInfo = { ...childInfo };

        const user = await User.findByIdAndUpdate(
            req.user.userId,
            { $set: updateFields },
            { new: true, runValidators: true }
        ).select('-password');

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({
            message: 'Profile updated successfully',
            user: {
                id: user._id,
                userName: user.userName,
                email: user.email,
                phone: user.phone,
                userType: user.userType,
                childInfo: user.childInfo
            }
        });
    } catch (error) {
        console.error('Error updating user profile:', error);
        res.status(500).json({ error: 'Failed to update profile' });
    }
});

module.exports = router;