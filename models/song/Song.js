const mongoose = require('mongoose')

const Song = mongoose.Schema({
    type:String
});

module.exports = {Song}