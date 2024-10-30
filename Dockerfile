FROM python:3.12

ARG PROMPTS_FILE_NAME=x_prompts.json

ENV PORT '8000'
ENV HOST '0.0.0.0'
ENV BIND "$HOST:$PORT"
ENV APP_NAME 'slack-beam'

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app app

COPY $PROMPTS_FILE_NAME .

VOLUME posts.db

VOLUME $PROMPTS_FILE_NAME

EXPOSE $PORT

CMD ["gunicorn", "app:app"]

