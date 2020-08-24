FROM python:3.7

COPY Pipfile* /
RUN pip install pipenv
RUN pipenv lock -r > /requirements.txt
RUN pip install -r /requirements.txt

COPY . /opt/square-api
WORKDIR /opt/square-api


EXPOSE 8001

ENTRYPOINT ["gunicorn", "--worker-tmp-dir", "/dev/shm"]
CMD ["--bind", "0.0.0.0:8001", "--timeout", "300", "app:api"]
