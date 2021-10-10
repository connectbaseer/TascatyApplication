FROM python:3.8.12-bullseye
ENV TZ=Asia/Dubai
RUN apt install -y curl default-libmysqlclient-dev
RUN pip install --upgrade pip
RUN pip install django==2.2
RUN pip install djangorestframework mysqlclient gunicorn
RUN mkdir -p apps/tascaty
WORKDIR /apps/tascaty 
RUN mkdir -p /apps/tascaty/run
COPY tascaty_src/. /apps/tascaty/.
COPY entrypoint.sh /apps/tascaty/run/.
RUN chmod u+x /apps/tascaty/run/entrypoint.sh
ENTRYPOINT [ "sh", "/apps/tascaty/run/entrypoint.sh"]