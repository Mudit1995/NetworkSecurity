# Base image
FROM python:3.12

# Set working directory
WORKDIR /app

COPY . /app 


RUN apt update -y && apt install awscli -y 

RUN apt-get update && pip install -r requirements.txt
# Placeholder for additional Dockerfile steps

# Command to run the application
CMD ["python3", "app.py"]
