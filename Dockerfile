FROM python:3.9.5

# Create app directory
WORKDIR /usr/src/app

COPY requirements.text /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app

EXPOSE 3000

CMD ["ENV=prod","DOCKER=1", "pytho3", "main.py"]
