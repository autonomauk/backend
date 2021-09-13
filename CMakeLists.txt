cmake_minimum_required(VERSION 3.11...3.19)

project(
  AutonomaBackend 
  VERSION 0.8.4
  DESCRIPTION "Backend server for Autonoma"
  LANGUAGES NONE
  HOMEPAGE_URL "https://spotify.janhendrikewers.uk")

set( VARS   
            PORT
            IP
            JWT_SECRET_KEY
            ENV
            SPOTIFY_CLIENT_ID
            SPOTIFY_CLIENT_SECRET
            SPOTIFY_REDIRECT_URI
            MONGODB_URI
            MONGODB_DB
)

foreach(VAR IN LISTS VARS)
    if(DEFINED ENV{${VAR}})
        set("${VAR}" $ENV{${VAR}})
        message(STATUS "Environmental variable ${VAR} set")
    else()
        message(FATAL_ERROR "Environmental variable ${VAR} not set")
    endif()    
endforeach(VAR)

foreach(VAR IN ITEMS CMAKE_PROJECT_HOMEPAGE_URL CMAKE_PROJECT_VERSION)
    message(STATUS "Environmental variable ${VAR} set")
endforeach(VAR)

configure_file(config/config.py.in config/config.py @ONLY)

configure_file(Autonoma.service.in Autonoma.service @ONLY)
install(FILES Autonoma.service DESTINATION /etc/systemd/system/ COMPONENT config)
