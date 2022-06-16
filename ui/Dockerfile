# Use temporary build container
FROM node:lts-alpine AS build
# make the 'app' folder the current working directory
WORKDIR /app
# copy 'package.json' to install dependencies
COPY package*.json ./
# install dependencies
RUN npm install
# copy files and folders to the current working directory (i.e. 'app' folder)
COPY . .
# build app for production with minification
RUN npm run build

# Build production container containing only the distribution
# The container can be used in a pod together with NGINX or
# Apache
FROM nginx:stable-alpine
COPY --from=build /app/dist/ /usr/share/nginx/html
