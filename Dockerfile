FROM python:3.9.5

# Create app directory
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
VOLUME .:/usr/src/app

EXPOSE 3001

CMD ["python3", ".", "--server","--env","development"]
