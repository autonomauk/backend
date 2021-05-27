const express = require("express");

const fetch = require('node-fetch');
const { User } = require("../models/user/User");

const routes = (app) => {
  const router = express.Router();

  router.post("/logout", function(req,res) {
    User.findByIdAndRemove(req.body.id, (err,user)=>{
      res.send("OK");
    });
  });

  router.get("/login", function (req, res) {
    var scopes = 'user-read-private user-library-read playlist-modify-public playlist-modify-private';
    res.redirect('https://accounts.spotify.com/authorize' +
      '?response_type=code' +
      '&client_id=' + process.env.SPOTIFY_CLIENT_ID +
      (scopes ? '&scope=' + encodeURIComponent(scopes) : '') +
      '&redirect_uri=' + encodeURIComponent(process.env.SPOTIFY_REDIRECT_URI));
  });

  router.get("/login/callback", function (req, res) {
    const buff = Buffer.from(process.env.SPOTIFY_CLIENT_ID + ":" + process.env.SPOTIFY_CLIENT_SECRET)
    const body = {
      "grant_type": "authorization_code",
      "code": req.query.code,
      "redirect_uri": process.env.SPOTIFY_REDIRECT_URI,
    };

    const headers = {
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
      "Authorization": "Basic " + buff.toString('base64')
    };

    fetch('https://accounts.spotify.com/api/token',
      {
        body: new URLSearchParams(body),
        headers: headers,
        method: "POST",
      }
    )
      .then(response => response.json())
      .then(response => {
        // Create the user and save it. Return the userid as part of the redirect to home to save it down the line.
        console.log(response)
        const access_token = response.access_token;
        const expires_in = response.expires_in;
        const refresh_token = response.refresh_token;

        fetch('https://api.spotify.com/v1/me',
          {
            headers: {
              "Authorization": "Bearer " + access_token
            }
          })
          .then(response => response.json())
          .then(response => {
            const display_name = response.display_name;


            User.findOneAndUpdate({ display_name: display_name }, {
              display_name: display_name,
              spotifyAuthDetails: {
                access_token: access_token,
                expires_in: expires_in,
                refresh_token: refresh_token
              }
            },
              {
                new:true,
                upsert: true
              },
              (error, user) => {                
                let redirectToHomePage = () => res.redirect('/?id=' + user._id);
                if (error) {
                  console.error(error.code)
                  switch (error.code) {
                    case 11000:
                      redirectToHomePage();
                      break;
                    default:
                      res.send(error);
                  }
                }
                else {
                  redirectToHomePage();
                }
              });
          }
          );
      })
      .catch(err => res.send(err));
  })


  //it's a prefix before api it is useful when you have many modules and you want to
  //differentiate b/w each module you can use this technique
  // app.use("/api", router);
  app.use("",router); // Handle this via nginx now
};
module.exports = routes;
