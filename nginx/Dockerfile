FROM nginx:1.21.5-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir /etc/nginx/certs
COPY /certs /etc/nginx/certs
