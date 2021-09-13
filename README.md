# Autonoma - Backend
[![Deploy backend](https://github.com/autonomauk/backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/autonomauk/backend/actions/workflows/deploy.yml)
[![Unit tests](https://github.com/autonomauk/backend/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/autonomauk/backend/actions/workflows/unittests.yml)
[![codecov](https://codecov.io/gh/autonomauk/backend/branch/master/graph/badge.svg?token=ZOHBKABCJ8)](https://codecov.io/gh/autonomauk/backend)

This repo contains the code for Autonoma's backend.

## Run

1. Install requirements with `python3 -m pip install -r requirements`
2. Run the server with `python3 . --server --env development`
3. Access the API at `localhost:3001`

For the best results use `docker-compose` in conjunction with the top-level repo https://github.com/autonomauk/autonoma.

## Documentation

Run `python3 . --server --env development` and head to http://localhost:3001/redoc. FastAPI automatically generates documentation using Swagger.
