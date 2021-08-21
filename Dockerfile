FROM python:3.7.9

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
ENV FLASK_APP=flaskr
ENV DB_USER=postgres
ENV DB_PASSWORD=password
ENV DB_HOST=127.0.0.1:5432
ENV PYTHONDONTWRITEBYTECODE 1

# ENTRYPOINT ["flask", "run"]
ENTRYPOINT ["gunicorn", "flaskr:create_app()"]
# CMD ["gunicorn", ""flask:create_app()""]
