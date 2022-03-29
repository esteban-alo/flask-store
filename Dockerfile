FROM python:3.10.4-slim-buster

WORKDIR /python-store

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP=wsgi.py

ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0"]