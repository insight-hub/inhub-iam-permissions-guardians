FROM python:3.11-slim as build

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY ./requirements.txt . 

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=build /app/wheels /wheels
COPY --from=build /app/requirements.txt .
RUN pip install --no-cache /wheels/* && \
    rm -rf /root/.cache/pip

COPY . .

EXPOSE 8000
CMD alembic upgrade head && \
    uvicorn "app.main:app" --host 0.0.0.0 --port 8000 
