FROM python:latest

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY /BoardRef/requirements.txt /app
RUN pip install -r requirements.txt

# Copy the application code
COPY /BoardRef /app

CMD ["python", "main.py"]