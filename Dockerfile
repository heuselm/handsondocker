FROM ubuntu:18.04
WORKDIR /app
COPY . /app
RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip \ 
    software-properties-common
RUN pip3 install tensorflow
RUN chmod +x index.py
CMD ["python3","index.py"]
