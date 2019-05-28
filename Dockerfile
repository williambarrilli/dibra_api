FROM python:2.7
ADD . /templates
WORKDIR /templates
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app_main.py"]