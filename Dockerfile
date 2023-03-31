FROM python:3.6
COPY app.py test.py logic.py /app/
WORKDIR /app
RUN pip install flask flask_restful xmlrunner pytest elastic-apm[flask] # This downloads all the dependencies
CMD ["python", "app.py"]
