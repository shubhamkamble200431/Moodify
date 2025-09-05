const mongoose = require("mongoose");

const songSchema = new mongoose.Schema({
    track_id: {
        type: String,
        required: true,
        unique: true
    },
    track_name: {
        type: String,
        required: true
    },
    album: {
        type: String,
        required: true
    },
    artists: {
        type: [String], // List of artists for collaborations
        required: true
    },
    release_year: {
        type: Number,
        required: true
    },
    likes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }],
    dislikes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }]
});

module.exports = mongoose.model("Song", songSchema);
