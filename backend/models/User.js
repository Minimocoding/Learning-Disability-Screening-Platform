const mongoose = require('mongoose');

const childInfoSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        trim: true,
        minlength: 2,
        maxlength: 100
    },
    age: {
        type: Number,
        required: true,
        min: 3,
        max: 18
    },
    schoolName: {
        type: String,
        required: true,
        trim: true,
        maxlength: 200
    },
    grade: {
        type: String,
        required: true,
        trim: true,
        maxlength: 50
    }
});

const userSchema = new mongoose.Schema({
    userType: {
        type: String,
        required: true,
        enum: ['parent', 'psychologist', 'teacher']
    },
    userName: {
        type: String,
        required: true,
        trim: true,
        minlength: 2,
        maxlength: 100
    },
    email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true,
        trim: true,
        match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'Please enter a valid email']
    },
    phone: {
        type: String,
        required: true,
        trim: true,
        match: [/^\+?[\d\s\-\(\)]+$/, 'Please enter a valid phone number']
    },
    password: {
        type: String,
        required: true,
        minlength: 6
    },
    childInfo: {
        type: childInfoSchema,
        required: true
    },
    isActive: {
        type: Boolean,
        default: true
    },
    lastLogin: {
        type: Date
    }
}, {
    timestamps: true
});

// Index for email lookup
userSchema.index({ email: 1 });

// Virtual for user display name
userSchema.virtual('displayName').get(function() {
    return `${this.userName} (${this.userType})`;
});

// Method to update last login
userSchema.methods.updateLastLogin = function() {
    this.lastLogin = new Date();
    return this.save();
};

module.exports = mongoose.model('User', userSchema);