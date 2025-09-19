const jwt = require('jsonwebtoken');
const User = require('../models/User');

const authenticateToken = async (req, res, next) => {
    try {
        // Get token from header
        const authHeader = req.header('Authorization');
        const token = authHeader && authHeader.replace('Bearer ', '');

        if (!token) {
            return res.status(401).json({ 
                error: 'Access denied. No token provided.' 
            });
        }

        // Verify token
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback-secret');
        
        // Check if user still exists and is active
        const user = await User.findById(decoded.userId);
        if (!user || !user.isActive) {
            return res.status(401).json({ 
                error: 'Token is not valid or user is inactive.' 
            });
        }

        // Add user info to request
        req.user = {
            userId: decoded.userId,
            userType: decoded.userType
        };

        next();
    } catch (error) {
        if (error.name === 'JsonWebTokenError') {
            return res.status(401).json({ 
                error: 'Invalid token.' 
            });
        } else if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ 
                error: 'Token expired.' 
            });
        }
        
        console.error('Auth middleware error:', error);
        res.status(500).json({ 
            error: 'Server error during authentication.' 
        });
    }
};

const requireRole = (roles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({ 
                error: 'Authentication required.' 
            });
        }

        if (!roles.includes(req.user.userType)) {
            return res.status(403).json({ 
                error: 'Insufficient permissions.' 
            });
        }

        next();
    };
};

module.exports = {
    authenticateToken,
    requireRole
};