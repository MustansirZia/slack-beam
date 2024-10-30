FROM python:3.12

ENV PORT '8000'
ENV HOST '0.0.0.0'
ENV BIND "$HOST:$PORT"
ENV APP_NAME 'slack-beam'

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app

VOLUME posts.db

EXPOSE $PORT

CMD ["gunicorn", "app:app"]

