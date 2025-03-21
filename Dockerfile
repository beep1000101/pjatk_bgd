# Use a Python 3.12.2 runtime as a parent image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the /app/data directory exists
RUN mkdir -p /app/data

# Copy the Python source code into the container
COPY python/ ./python/

# Copy the data directory into the container
COPY data/ /app/data/

# Make the script executable
CMD ["python", "./python/read.py"]
