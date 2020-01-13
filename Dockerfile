# Pull python base image
FROM python:3.7.4-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Copy Project to the container
RUN mkdir -p /fyle-accounting-credentials-generator
COPY . /fyle-accounting-credentials-generator/
WORKDIR /fyle-accounting-credentials-generator


# Expose development port
EXPOSE 8000

# Run development server
CMD /bin/bash run.sh