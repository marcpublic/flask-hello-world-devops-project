FROM python:3.6
COPY app.py test.py default.html /app/
WORKDIR /app
RUN pip install flask pytest elastic-apm[flask] # This downloads all the dependencies
CMD ["python", "app.py"]
