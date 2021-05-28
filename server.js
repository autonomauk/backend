require('custom-env').env(true)

const express = require("express");
// const path = require("path");
const cookieParser = require("cookie-parser");
const bodyParser = require("body-parser");
const cors = require("cors");
const db = require("./db");

const mongoose = require("mongoose");
mongoose.set('useFindAndModify', false);


const app = express();

//connection from db here
db.connect(app);

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
//app.use(express.static(path.join(__dirname, "public")));

// logger handler
var logger = function(req,res,next){
    console.log("Call to ", req.baseUrl + req.path);
    console.log("   Body:   ", req.body);
    console.log("   Params: ", req.params);
    console.log("   Method: ", req.method);
    next();
};
app.use(logger);

const cron = require("node-cron");
const worker = require("./worker");
cron.schedule(
  '0 * * * * *', // Every minute
  () => worker()
);

//  adding routes
require("./routes")(app);

app.on("ready", () => {
  app.listen(process.env.PORT, () => {
    console.log("Server is up on port", process.env.PORT);
  });
});

module.exports = app;
