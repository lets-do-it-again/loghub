FROM python:latest


# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/product.txt .
RUN pip install -r product.txt



COPY ./docker/django/start.sh /start.sh
RUN chmod +x /start.sh


# copy project
COPY ./loghub .