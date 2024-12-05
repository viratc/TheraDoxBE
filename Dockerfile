# Pull official base image
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disc and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "app.src.v1.main:fastapi_app", "--host", "0.0.0.0", "--port", "8000"]