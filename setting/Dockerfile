FROM ubuntu:latest
MAINTAINER Dilshat Salikhov "d.salikhov@innopolis.com"
RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install flask
RUN mkdir project \
    && cd project \
    && git clone https://github.com/ssd-courseproject/adminssion-forms-backend.git
WORKDIR project/adminssion-forms-backend
ENTRYPOINT ["python"]
CMD ["app.py"]