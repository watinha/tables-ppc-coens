FROM python:3.13.0-alpine3.20

ADD . /app

WORKDIR /app

RUN pip install pandas \
		chevron

CMD ["python", "main.py"]
