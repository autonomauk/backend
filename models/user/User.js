const { SpotifyAuthDetailsSchema } = require("../spotifyAuthDetails/SpotifyAuthDetails");
const {Song} = require("../song/Song");
const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    user_id:{
        type: String
    },
    display_name: {
        type: String,
        index: true
    },
    spotifyAuthDetails: {
        type: SpotifyAuthDetailsSchema,
        required: true
    }
}, {
    timestamps: true
});

const User = mongoose.model('User', UserSchema);

module.exports = { User };
