# Use Nginx as a base image
FROM nginx:alpine

# Copy the static files into the Nginx server directory
COPY ./dashboard /usr/share/nginx/html/dashboard
COPY ./login /usr/share/nginx/html/login

# Expose port 80 to the outside world
EXPOSE 80