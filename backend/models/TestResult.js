const mongoose = require('mongoose');

const testResultSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    answers: {
        type: [Number],
        required: true,
        validate: {
            validator: function(arr) {
                return arr.length === 50 && arr.every(answer => [0, 1, 2].includes(answer));
            },
            message: 'Must provide exactly 50 answers with values 0, 1, or 2'
        }
    },
    results: {
        hasLearningDifference: {
            type: Boolean,
            required: true
        },
        primaryType: {
            type: String,
            enum: ['dyslexia', 'dyscalculia', 'dysgraphia', null],
            default: null
        },
        categoryScores: {
            dyslexia: {
                type: Number,
                required: true,
                min: 0
            },
            dyscalculia: {
                type: Number,
                required: true,
                min: 0
            },
            dysgraphia: {
                type: Number,
                required: true,
                min: 0
            }
        },
        totalScore: {
            type: Number,
            required: true,
            min: 0,
            max: 100
        },
        mentalHealthFlag: {
            type: Boolean,
            default: false
        },
        confidence: {
            type: Number,
            required: true,
            min: 0,
            max: 1
        }
    },
    mlModelVersion: {
        type: String,
        default: 'v1.0-basic'
    },
    submittedAt: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

// Indexes for efficient querying
testResultSchema.index({ userId: 1, submittedAt: -1 });
testResultSchema.index({ 'results.hasLearningDifference': 1 });
testResultSchema.index({ 'results.primaryType': 1 });

// Virtual for test summary
testResultSchema.virtual('summary').get(function() {
    return {
        hasLD: this.results.hasLearningDifference,
        type: this.results.primaryType,
        score: this.results.totalScore,
        date: this.submittedAt
    };
});

// Method to get human-readable result
testResultSchema.methods.getReadableResult = function() {
    const result = this.results;
    let summary = '';
    
    if (result.hasLearningDifference) {
        summary = `Learning difference likely detected. Primary indication: ${result.primaryType || 'Mixed profile'}.`;
        if (result.mentalHealthFlag) {
            summary += ' Mental health support recommended.';
        }
    } else {
        summary = 'No significant learning difference indicators detected.';
    }
    
    return summary;
};

module.exports = mongoose.model('TestResult', testResultSchema);