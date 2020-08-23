FROM python:3.7

COPY . /opt/square-api
WORKDIR /opt/square-api

COPY Pipfile /opt/square-api
RUN pip install pipenv
RUN pipenv lock -r > /requirements.txt
RUN pip install -r /requirements.txt

EXPOSE 8001

ENTRYPOINT ["gunicorn", "--worker-tmp-dir", "/dev/shm"]
CMD ["--bind", "0.0.0.0:8001", "--timeout", "300", "app:api"]
