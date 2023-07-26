# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI application into the container
#COPY requirements.txt /app/
COPY testtest.py .
COPY python-api-project-393719-93fac9224067.json /app/credentials/

EXPOSE 8080

# Start the FastAPI application when the container starts
CMD ["uvicorn", "testtest:app", "--host", "0.0.0.0", "--port", "8080"]