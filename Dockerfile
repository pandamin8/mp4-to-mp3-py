# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Create a directory for the application
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . /app/

# Expose the port that the app runs on
EXPOSE 5001

# Define the command to run the application
CMD ["waitress-serve", "--port=5001", "--call", "app:create_app"]