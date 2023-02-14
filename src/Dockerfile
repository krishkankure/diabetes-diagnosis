# app/Dockerfile

FROM ubuntu:latest
WORKDIR /src/
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++ \
        git && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get install libgomp1 -y

FROM python:3.10.0-slim-buster

WORKDIR /src

COPY requirements.txt /src/

COPY --from=0 /src ./
RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /src/
ENTRYPOINT ["streamlit", "run"]
CMD [ "stream.py" ]


# COMMANDS:
# docker build -t diabetes:latest .
# docker run -p 8501:8501 diabetes:latest
