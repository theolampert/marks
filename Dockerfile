FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP=server.py
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]
