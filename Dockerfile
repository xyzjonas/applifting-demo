FROM python:3.10.1-alpine as base-image

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# Just for the sake of this demo and a slimmer image.
RUN pip install psycopg2-binary


FROM python:3.10-alpine as build-stage

COPY . .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry build



FROM base-image

WORKDIR app

COPY --from=build-stage dist/*.whl wheels/
RUN pip install wheels/*

EXPOSE 8000

ENTRYPOINT ["applifting-demo"]
