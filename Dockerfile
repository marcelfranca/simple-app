FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/app
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

WORKDIR /usr/app
COPY . /usr/app

EXPOSE 5000:5000

CMD ["python", "app.py"]
