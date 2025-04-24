FROM bitnami/spark:latest

USER root
RUN apt-get update && apt-get install -y python3-pip && pip3 install requests && pip3 install pandas && pip3 install numpy

USER 1001
