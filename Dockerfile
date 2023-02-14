# Use an official Python runtime as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python packages listed in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app code to the container
COPY . .


CMD ["python3", "app.py"]
