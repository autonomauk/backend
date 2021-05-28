const SpotifyWebApi = require('spotify-web-api-node');
const { User } = require('../../models/user/User');

class SpotifyHelper {
    constructor(spotifyAuthDetails, username, id) {
        this.spotifyApi = new SpotifyWebApi({
            clientId: process.env.SPOTIFY_CLIENT_ID,
            clientSecret: process.env.SPOTIFY_CLIENT_SECRET,
            redirectUri: process.env.SPOTIFY_REDIRECT_URI,

            accessToken: spotifyAuthDetails.access_token,
            refreshToken: spotifyAuthDetails.refresh_token
        })
        this.username = username;
        this.id = id
    }

    refreshToken() {
        console.log("Refreshing access token for "+this.username);
        this.spotifyApi.refreshAccessToken().then(data => {
            const access_token = data.body['access_token'];
            this.spotifyApi.setAccessToken(access_token)
            User.findByIdAndUpdate(this.id,{
                spotifyAuthDetails:{
                    access_token:access_token,
                    refresh_token:this.spotifyApi.getRefreshToken(),
                    expires_in:data.body['expires_in']
                }
            },(err,user)=>{})
        })
    }
}





module.exports = { SpotifyHelper }
