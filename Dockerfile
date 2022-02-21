# Official Docker python image
FROM python:3.8-slim-buster as base

# Setup No buffer for python output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update python pip
RUN pip install --upgrade pip
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


# Setup working directory
RUN mkdir -p /netflix_demo
WORKDIR /netflix_demo

# Add Files
ADD src /netflix_demo/src/
COPY requirements.txt /netflix_demo/
COPY init.sh /netflix_demo/

# Make scripts executable
RUN chmod +x /netflix_demo/init.sh

# Install project dependencies
RUN pip install -r /netflix_demo/requirements.txt
# RUN --mount=type=cache,target=/root/.cache/pip pip install -r /netflix_demo/requirements.txt

# Expose ports
EXPOSE 8000