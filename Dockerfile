# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Create directories for SSL certificates and key
RUN mkdir -p /app/certs /app/key

# Copy SSL certificates to the container
COPY xdba_certificate.pem /app/certs/
COPY test.pem /app/key/



# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches with SSL support
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-keyfile", "/app/key/test.pem", "--ssl-certfile", "/app/certs/xdba_certificate.pem"]