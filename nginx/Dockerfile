FROM nginx
COPY tascaty.conf /etc/nginx/conf.d/default.conf
RUN mkdir -p /apps/tascaty/static
COPY static/. /apps/tascaty/static/.