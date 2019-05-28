FROM python:3.6
ADD . /models
WORKDIR /models
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app_main.py"]