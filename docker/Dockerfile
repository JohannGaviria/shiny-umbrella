FROM python:3.12.7-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN  apk update \
	&& apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
	&& pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

COPY ./docker/entrypoint.sh /app/entrypoint.sh 

CMD ["sh", "docker/entrypoint.sh"]