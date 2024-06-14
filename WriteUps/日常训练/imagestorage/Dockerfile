FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt upgrade -y
RUN apt install apache2 php -y

RUN rm -rf /var/www/html/index.html

COPY ./images /var/www/html/images
COPY ./src/ /var/www/html/
COPY ./flag /flag

RUN chmod 111 /flag

ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]