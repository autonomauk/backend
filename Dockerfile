# Create image based on the official Python image from dockerhub
FROM python:3.9.5

# Create app directory
WORKDIR /usr/src/app

# Copy requirements definition
COPY requirements.txt /usr/src/app/requirements.txt

#Instlal requirements
RUN pip install -r requirements.txt

# Redefine $APP_PATH otherwise its value is not passed through
arg APP_PATH
VOLUME ${APP_PATH}/backend:/usr/src/app

# Expose the port the app runs in
EXPOSE 3001

# Serve the app
CMD ["python3", ".", "--server","--env","development"]
