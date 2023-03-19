# Set base image for the container, official Python 3.9 slim-buster image.
FROM python:3.8-slim-buster

# Set the Label maintainer
LABEL maintainer="Min"
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# Set the working directory for the container to /app
WORKDIR /app

# Copy contents of current directory to containers working directory
COPY . /app

# Install dependencies required by the application, which are listed
RUN python -m pip install --upgrade pip
# in the "requirements.txt" file in the current directory
RUN pip install --no-cache-dir -r requirements.txt
# Expose port 8000 for FastAPI to listen on
EXPOSE 8000

# Start the FastAPI application using the uvicorn server,
# with the main module named main and the FastAPI instance named app,
# listening on port 8000 and accepting connections from
# any IP address (0.0.0.0).
CMD ["uvicorn", "main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]
# CMD ["python3", "main.py"]