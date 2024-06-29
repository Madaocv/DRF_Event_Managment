# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=app.settings
ENV PYTHONUNBUFFERED=1

# Run the Django application
CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata initial_data.json && python manage.py runserver 0.0.0.0:8000"]
