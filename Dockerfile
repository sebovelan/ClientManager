# Set working directory in the container
WORKDIR \clientSystem

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

# Set environment variables 
ENV PYTHONUNBUFFERED=1 
    DJANGO_SETTINGS_MODULE=clientSystem.settings.py

# Expose port 8000 (Django’s default)
EXPOSE 8000

# Run the Django server
CMD [python, manage.py, runserver, 0.0.0.0:8080]