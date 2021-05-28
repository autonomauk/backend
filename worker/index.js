const { User } = require('../models/user/User');
const { SpotifyHelper } = require('../utils/helpers/spotify');
const moment = require('moment');
const { default: fetch } = require('node-fetch');

const worker = async () => {
    console.log("Starting worker at "+new moment().format());

    const playlistName = moment().format('MMMM YY');

    const users = await User.find({}).exec();
    users.forEach(user => {
        const spotifyHelper = new SpotifyHelper(user.spotifyAuthDetails, user.display_name, user._id);

        spotifyHelper.spotifyApi.getUserPlaylists(user.display_name, { limit: 50 }).then(playlists => {
            const playlistInd = playlists.body.items.findIndex((playlist => playlist.name === playlistName));
            if (playlistInd > -1) {
                findSongsAndAdd(user.display_name, spotifyHelper, playlists.body.items[playlistInd].id);
            } else {
                if ((playlists.body.total - playlists.body.limit) > 0) {
                    spotifyHelper.spotifyApi.getUserPlaylists(user.display_name, { limit: 50, offset: playlists.body.offset + playlists.body.limit }).then(playlists => {
                        const playlistInd = playlists.body.items.findIndex((playlist => playlist.name === playlistName));
                        if (playlistInd > -1) {
                            findSongsAndAdd(user.display_name, spotifyHelper, playlists.body.items[playlistInd].id);
                        } else {
                            console.error("No playlist with name " + playlistName + " found for " + user.display_name);
                            spotifyHelper.spotifyApi.createPlaylist(playlistName).then(playlist => findSongsAndAdd(user.display_name, spotifyHelper, playlist.body.id))
                                .catch(err => handleErrors(err, spotifyHelper));
                        }
                    })
                        .catch(err => handleErrors(err, spotifyHelper));
                } else {
                    console.error("No playlist with name " + playlistName + " found for " + user.display_name);
                    spotifyHelper.spotifyApi.createPlaylist(playlistName).then(playlist => findSongsAndAdd(user.display_name, spotifyHelper, playlist.body.id))
                        .catch(err => handleErrors(err, spotifyHelper));
                }
            }
        })
        .catch(err => handleErrors(err, spotifyHelper));
    });
};

const findSongsAndAdd = async (display_name, spotifyHelper, playlistId) => {
    const existingTracks = await spotifyHelper.spotifyApi.getPlaylistTracks(playlistId, { fields: 'items.track.uri' })
        .then(res => res.body.items)
        .then(tracks => tracks.map(track => track.track.uri))
        .catch(err => handleErrors(err, spotifyHelper));


    const savedTracks = await findMonthlySavedTracks(spotifyHelper);

    const freshTracks = savedTracks.filter(savedTrack => !existingTracks.find((val, ind) => savedTrack === val))

    if (freshTracks.length > 0) {
        console.log("Adding " + freshTracks.length + " tracks to playlist for " + display_name);
        spotifyHelper.spotifyApi.addTracksToPlaylist(playlistId, freshTracks)
            .catch(err => handleErrors(err, spotifyHelper));
    }
};

const findMonthlySavedTracks = async (spotifyHelper) => {
    return spotifyHelper.spotifyApi.getMySavedTracks({ limit: 50, offset: 0 })
        .then(tracks => tracks.body.items)
        .then(tracks => tracks.filter(track => {
            const added_at = moment(track.added_at, "YYYY MM DD hh:mm:ss");
            if (added_at.isSame(new Date(), "month")) {
                return true;
            }
            return false;
        }))
        .then(tracks => tracks.map(track => track.track.uri))
        .catch(err => handleErrors(err, spotifyHelper));
}

const handleErrors = async (error, spotifyHelper) => {
    switch (error.statusCode) {
        case 401:
            switch (error.body.error.message) {
                case "The access token expired":
                    spotifyHelper.refreshToken();
                    break;
            }
            break;
        default:
            console.error(error)
    }

}

module.exports = worker;
