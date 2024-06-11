from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import os
from elevenlabs.client import ElevenLabs

# Initialize FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Retrieve the API key (normally you would get this from an environment variable for security)
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

        # Save the generated audio to a file (you can modify this part to return the audio as a response)
        audio_file_path = "output_audio.wav"
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        logging.info(f"Audio successfully saved to {audio_file_path}")
        return {"message": "Audio successfully generated and saved."}

    except Exception as e:
        logging.error(f"Failed to generate audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {e}")

# Run the FastAPI app using Uvicorn if this script is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
