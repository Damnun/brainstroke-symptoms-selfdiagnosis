FROM python:3.8

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD templates templates

ADD face-recognition-py.py .

CMD ["python", "app.py"]