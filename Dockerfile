# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY logalanche.py .

# Copy the default logs.json into the container
COPY logs.json .

# Set default environment variables (overridable by user)
ENV DD_API_KEY=""

# logalanche's own logs: 'stdout', 'none', 'file'
ENV LOG_MODE="stdout"

# Command to run the Python script
CMD ["python", "logalanche.py"]

