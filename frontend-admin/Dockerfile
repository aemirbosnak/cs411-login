# Use Nginx as a base image
FROM nginx:alpine

# Copy the static files into the Nginx server directory
COPY ./dashboard /usr/share/nginx/html/dashboard
COPY ./login /usr/share/nginx/html/login
COPY ./inpatient-management /usr/share/nginx/html/inpatient-management
COPY ./admitted-patients /usr/share/nginx/html/admitted-patients
COPY ./components /usr/share/nginx/html/components

# Expose port 80 to the outside world
EXPOSE 80