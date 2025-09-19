const mongoose = require('mongoose');

const questionSchema = new mongoose.Schema({
    questionNumber: {
        type: Number,
        required: true,
        unique: true,
        min: 1,
        max: 50
    },
    questionText: {
        type: String,
        required: true,
        trim: true,
        maxlength: 500
    },
    category: {
        type: String,
        required: true,
        enum: ['dyslexia', 'dyscalculia', 'dysgraphia']
    },
    options: {
        no: {
            type: String,
            default: "No (it doesn't happen)",
            required: true
        },
        sometimes: {
            type: String,
            default: "Sometimes (sometimes it happens)",
            required: true
        },
        yes: {
            type: String,
            default: "Yes (it happens)",
            required: true
        }
    },
    active: {
        type: Boolean,
        default: true
    },
    createdBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }
}, {
    timestamps: true
});

// Index for efficient querying
questionSchema.index({ questionNumber: 1 });
questionSchema.index({ category: 1 });
questionSchema.index({ active: 1 });

module.exports = mongoose.model('Question', questionSchema);