#!/bin/bash
docker build -t ghcr.io/ingos11/flaskapp:main .
docker build -t ghcr.io/ingos11/vuejsui:latest ui/.
