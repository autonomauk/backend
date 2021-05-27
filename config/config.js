const env = process.env.NODE_ENV || "dev";
const docker = process.env.DOCKER || false;

var key;

if (env === "dev"){
    if(docker){
        key = "dev_docker";
    } else {
        key = "dev_local";
    }
} else {
    throw "Unknown config";
}

const config = require("./config.json");
const envConfig = config[key];
console.log(envConfig);

Object.keys(envConfig).forEach((key) => {
  process.env[key] = envConfig[key];
});