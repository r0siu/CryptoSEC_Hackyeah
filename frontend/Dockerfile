# to build docker image before usage: `docker build -t frontend-image .`
FROM nginx:latest

# Copy frontend application code into NGINX's HTML directory
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
