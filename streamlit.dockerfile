
FROM python:latest

WORKDIR /opt/app

COPY ./Streamlit .
RUN pip install --no-cache-dir -r requirements.txt
