FROM python:3

WORKDIR /opt/app

COPY ./Streamlit .
RUN pip install --no-cache-dir -r requirements.txt
