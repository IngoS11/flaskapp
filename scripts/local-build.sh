#!/bin/bash
# build the python docker container
docker build -t ghcr.io/ingos11/flaskapp:main .

# run npm build and the create the docker container from it
cd ui
npm install
npm run build --if-present
docker build -t ghcr.io/ingos11/vuejsui:latest .
