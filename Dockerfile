# Use an official Python runtime as a parent image
FROM python3.10-slim-buster

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
# This is where your code will live inside the Docker container
WORKDIR app

# Install system dependencies (needed for psycopg2-binary)
RUN apt-get update && apt-get install -y 
    postgresql-client 
    gcc 
    # Clean up APT cache to reduce image size
    && rm -rf varlibaptlists

# Copy the requirements file into the working directory
COPY requirements.txt app

# Install Python dependencies
# Use --no-cache-dir to avoid storing build artifacts, reducing image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the working directory
# .dockerignore will prevent copying unnecessary files (like venv, .git, .env)
COPY . app

# Expose the port that Gunicorn will listen on
# HAProxy will forward traffic to this port
EXPOSE 8000

# Define the command to run your application using Gunicorn
# This will be the default command executed when the container starts
# --bind 0.0.0.08000 makes Gunicorn listen on all network interfaces on port 8000
# --workers 3 sets the number of Gunicorn worker processes (adjust based on your CPU cores)
# clientSystem.wsgiapplication points to your WSGI application
CMD [gunicorn, clientSystem.wsgiapplication, --bind, 0.0.0.08000, --workers, 3]