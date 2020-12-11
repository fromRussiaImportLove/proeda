FROM python:3.8.5

WORKDIR /code
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
