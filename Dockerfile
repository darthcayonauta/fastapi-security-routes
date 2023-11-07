FROM python:3.8

WORKDIR /app

COPY dbClass.py main3.py ./

RUN pip install fastapi uvicorn pymongo jose python-jose httpx passlib python-multipart

ENV HOST_NAME=mongoz

EXPOSE 8000

CMD [ "uvicorn","main3:app","--host","0.0.0.0","--port","8000"]