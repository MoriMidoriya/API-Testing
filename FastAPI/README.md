# FastAPI Audio Generation with ElevenLabs and MongoDB

## Overview
This project demonstrates how to use FastAPI along with the ElevenLabs API to generate audio from text input and store the generated audio in a MongoDB database. The example includes creating an endpoint in FastAPI, testing it using Postman, and integrating with ElevenLabs for audio generation.

## Requirements
- Docker
- Postman (optional for testing)

## Usage

### Running with Docker

1. *Build the Docker image:*
    sh
    docker build -t testelevenapi .
    

2. *Run the Docker container:*
    sh
    docker run -d -p 8000:8000 -e ELEVEN_API_KEY=your_actual_api_key_here -e MONGODB_URL=your_mongodb_url_here testelevenapi
    
    Replace your_actual_api_key_here with your actual ElevenLabs API key and your_mongodb_url_here with your MongoDB connection URL.

3. *Expose your local server to the internet using ngrok:*
    sh
    ngrok http 8000
    
    Copy the generated ngrok URL (e.g., https://<your-ngrok-subdomain>.ngrok-free.app).

4. *Use Postman to send the POST request using the ngrok URL:*

    *Enter the URL:*
    
    https://<your-ngrok-subdomain>.ngrok-free.app/generate-audio/
    

    **Set the Method to POST.**

    *Add Headers:*
    - Key: Content-Type
    - Value: application/json

    *Set the Body:*
    - Select raw.
    - Choose JSON.
    - Paste the JSON:
      json
      {
          "text": "Hello, when this thingy starts working, imma finally go to sleep. So please work",
          "voice": "Rachel",
          "model": "eleven_multilingual_v2"
      }
      

    *Send the Request:*
    Click Send in Postman and check the response.

### Stopping the Docker Container

1. *List running containers:*
    sh
    docker ps
    

2. *Stop the container:*
    sh
    docker stop <container_id>
    
    Replace <container_id> with the actual container ID.

3. *Optional: Remove the container:*
    sh
    docker rm <container_id>
    

### Copying the Audio File from Docker Container

1. *List running containers:*
    sh
    docker ps
    

2. *Copy the file from the container:*
    sh
    docker cp <container_id>:/app/output_audio.wav ./output_audio.wav
    
    Replace <container_id> with the actual container ID. This command will copy output_audio.wav from the /app directory inside the container to the current directory on your host machine.