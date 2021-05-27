const mongoose = require('mongoose');

const SpotifyAuthDetailsSchema = mongoose.Schema({
    _id:false,
    access_token:{
        type:String,
        required:true
    },
    expires_in:{
        type:Number,
        required:true
    },
    refresh_token:{
        type:String,
        required:true
    }
},
{
    timestamps:true
});

module.exports = {SpotifyAuthDetailsSchema};