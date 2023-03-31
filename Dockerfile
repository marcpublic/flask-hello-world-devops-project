FROM python:3.6
COPY app.py test.py /app/
WORKDIR /app
RUN pip install flask flask_restful xmlrunner pytest # This downloads all the dependencies
CMD ["python", "app.py"]
