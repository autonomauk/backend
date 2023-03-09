# Create image based on the official Python image from dockerhub
FROM python:3.10

# Create app directory
WORKDIR /usr/src/app

# Copy requirements definition
COPY requirements.txt /usr/src/app/requirements.txt

#Instlal requirements
RUN pip install -r requirements.txt

COPY . ./