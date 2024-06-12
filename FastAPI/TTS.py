import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from elevenlabs.client import ElevenLabs
from pymongo import MongoClient
from bson.binary import Binary

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Retrieve the API key from environment variables
api_key = os.getenv("ELEVEN_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the ELEVEN_API_KEY environment variable.")

# Initialize the ElevenLabs client
try:
    client = ElevenLabs(api_key=api_key)
    logging.info("ElevenLabs client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize ElevenLabs client: {e}")
    raise

# Retrieve MongoDB connection details from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
mongo_db_name = os.getenv("MONGO_DB_NAME", "audio_database")
mongo_collection_name = os.getenv("MONGO_COLLECTION_NAME", "audio_files")

# Initialize MongoDB client
try:
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client[mongo_db_name]
    mongo_collection = mongo_db[mongo_collection_name]
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise

# Model for the request body
class TextToSpeechRequest(BaseModel):
    text: str
    voice: Optional[str] = "Rachel"
    model: Optional[str] = "eleven_multilingual_v2"

# Endpoint to generate audio from text
@app.post("/generate-audio/")
async def generate_audio(request: TextToSpeechRequest):
    try:
        logging.info("Attempting to generate audio...")

        # Generate the audio data
        audio_generator = client.generate(
            text=request.text,
            voice=request.voice,
            model=request.model
        )

        logging.info("Audio generation request sent successfully.")

        # Convert the generator to bytes
        audio_bytes = b''.join(audio_generator)
        logging.info("Audio generator successfully converted to bytes.")

        # Store the generated audio in MongoDB
        audio_data = {
            "text": request.text,
            "voice": request.voice,
            "model": request.model,
            "audio": Binary(audio_bytes)
        }
        result = mongo_collection.insert_one(audio_data)

        logging.info(f"Audio successfully stored in MongoDB with id {result.inserted_id}")
        return {"message": "Audio successfully generated and stored in MongoDB.", "id": str(result.inserted_id)}

    except Exception as e:
        logging.error(f"Failed to generate audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {e}")

# Run the FastAPI app using Uvicorn if this script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
