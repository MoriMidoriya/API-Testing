# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Set environment variables
ENV ELEVEN_API_KEY=${ELEVEN_API_KEY}
ENV MONGODB_URL=${MONGODB_URL}

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "TTS:app", "--host", "0.0.0.0", "--port", "8000"]
