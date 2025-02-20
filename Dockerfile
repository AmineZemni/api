# Use Python base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy the requirements file explicitly to /app/
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app/

# Run the application (adjust command based on your app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
