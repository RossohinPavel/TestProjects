FROM nginx:1.27-alpine

EXPOSE 80/tcp
EXPOSE 443/tcp

COPY nginx.conf /etc/nginx/nginx.conf

CMD nginx -g 'daemon off;'
