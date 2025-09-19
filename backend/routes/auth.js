const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const router = express.Router();

// @route   POST /api/auth/register
// @desc    Register a new user
// @access  Public
router.post('/register', [
    body('userType').isIn(['parent', 'psychologist', 'teacher']).withMessage('Invalid user type'),
    body('userName').trim().isLength({ min: 2 }).withMessage('Name must be at least 2 characters'),
    body('email').isEmail().normalizeEmail().withMessage('Please enter a valid email'),
    body('phone').isMobilePhone().withMessage('Please enter a valid phone number'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
    body('childName').trim().isLength({ min: 2 }).withMessage('Child name must be at least 2 characters'),
    body('childAge').isInt({ min: 3, max: 18 }).withMessage('Child age must be between 3 and 18'),
    body('schoolName').trim().notEmpty().withMessage('School name is required'),
    body('grade').trim().notEmpty().withMessage('Grade/Standard is required')
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

        const {
            userType,
            userName,
            email,
            phone,
            password,
            childName,
            childAge,
            schoolName,
            grade
        } = req.body;

        // Check if user already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ 
                error: 'User already exists with this email address' 
            });
        }

        // Hash password
        const salt = await bcrypt.genSalt(12);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Create new user
        const user = new User({
            userType,
            userName,
            email,
            phone,
            password: hashedPassword,
            childInfo: {
                name: childName,
                age: childAge,
                schoolName,
                grade
            }
        });

        await user.save();

        // Generate JWT
        const token = jwt.sign(
            { userId: user._id, userType: user.userType },
            process.env.JWT_SECRET || 'fallback-secret',
            { expiresIn: '24h' }
        );

        res.status(201).json({
            message: 'User registered successfully',
            token,
            user: {
                id: user._id,
                userName: user.userName,
                email: user.email,
                userType: user.userType,
                childInfo: user.childInfo
            }
        });
    } catch (error) {
        console.error('Registration error:', error);
        res.status(500).json({ error: 'Failed to register user' });
    }
});

// @route   POST /api/auth/login
// @desc    Login user
// @access  Public
router.post('/login', [
    body('email').isEmail().normalizeEmail().withMessage('Please enter a valid email'),
    body('password').exists().withMessage('Password is required')
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

        const { email, password } = req.body;

        // Find user
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ 
                error: 'Invalid credentials' 
            });
        }

        // Check password
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(400).json({ 
                error: 'Invalid credentials' 
            });
        }

        // Generate JWT
        const token = jwt.sign(
            { userId: user._id, userType: user.userType },
            process.env.JWT_SECRET || 'fallback-secret',
            { expiresIn: '24h' }
        );

        res.json({
            message: 'Login successful',
            token,
            user: {
                id: user._id,
                userName: user.userName,
                email: user.email,
                userType: user.userType,
                childInfo: user.childInfo
            }
        });
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Failed to login' });
    }
});

// @route   GET /api/auth/verify
// @desc    Verify JWT token
// @access  Private
router.get('/verify', async (req, res) => {
    try {
        const token = req.header('Authorization')?.replace('Bearer ', '');
        
        if (!token) {
            return res.status(401).json({ error: 'No token provided' });
        }

        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback-secret');
        const user = await User.findById(decoded.userId).select('-password');
        
        if (!user) {
            return res.status(401).json({ error: 'Token is not valid' });
        }

        res.json({
            valid: true,
            user: {
                id: user._id,
                userName: user.userName,
                email: user.email,
                userType: user.userType,
                childInfo: user.childInfo
            }
        });
    } catch (error) {
        console.error('Token verification error:', error);
        res.status(401).json({ error: 'Token is not valid' });
    }
});

module.exports = router;