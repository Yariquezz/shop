###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-alpine as builder

# create directory for the app user
RUN mkdir -p /home/shop

# create the app user
RUN addgroup -S shop && adduser -S shop -G shop

# create the appropriate directories
ENV HOME=/home/shop
ENV SHOP_HOME=/home/shop/shop
RUN mkdir $SHOP_HOME
WORKDIR $SHOP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install --upgrade pip \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && pip install Pillow

# lint
RUN pip install --upgrade pip
RUN pip install flake8
RUN pip install coverage
COPY . .
RUN flake8 --ignore=E501,F401 .
RUN coverage erase
RUN coverage run manage.py test

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /home/shop/shop/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /home/shop

# create the app user
RUN addgroup -S shop && adduser -S shop -G shop

# create the appropriate directories
ENV HOME=/home/shop
ENV SHOP_HOME=/home/shop/shop
RUN mkdir $SHOP_HOME
WORKDIR $SHOP_HOME

# install dependencies
RUN apk update && apk add libpq jpeg-dev zlib-dev libjpeg
COPY --from=builder /home/shop/shop/wheels /wheels
COPY --from=builder /home/shop/shop/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $SHOP_HOME

# copy project
COPY . $SHOP_HOME

# chown all the files to the app user
RUN chown -R shop:shop $SHOP_HOME
RUN mkdir -p /home/shop/shop/static
RUN mkdir -p /home/shop/shop/media

RUN chown -R shop:root /home/shop/shop/static
RUN chown -R shop:root /home/shop/shop/media
RUN chown -R shop:root /usr/local/lib/python3.8/site-packages/jet/migrations/
# change to the app user
USER shop

# run entrypoint.sh
ENTRYPOINT ["/home/shop/shop/entrypoint.sh"]