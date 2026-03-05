
from dotenv import load_dotenv
load_dotenv()
import requests
import os
import base64

# --- Configuration ---
# IMPORTANT: Replace with your actual Sarvam AI TTS API Key
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "sk_hw54y565_zgntaPrOQpwghahJoab53TIR") 
# IMPORTANT: Replace with the actual Sarvam AI TTS API endpoint URL
# (This is a placeholder, please refer to Sarvam AI documentation for the correct URL)
SARVAM_API_ENDPOINT = "https://api.sarvam.ai/text-to-speech" 

# The Telugu story to convert to speech
STORY_TEXT = """ఒక దట్టమైన అడవిలో ఒక బలమైన సింహం ఉండేది. అది ప్రతిరోజూ అడవిలోని జంతువులను వేటాడేది. ఒకరోజు ఒక చిన్న కుందేలు వంతు వచ్చింది. ఆ కుందేలు చాలా తెలివైనది. అది సింహం దగ్గరకు ఆలస్యంగా వెళ్లింది. సింహం కోపంగా ఎందుకు ఆలస్యమైందని అడిగింది. అప్పుడు కుందేలు, "రాజా, దారిలో నాకు మరొక సింహం కనిపించింది, అది మిమ్మల్ని సవాలు చేస్తోంది" అని చెప్పింది. సింహం ఆవేశంతో కుందేలును ఆ మరొక సింహం దగ్గరకు తీసుకెళ్లమని కోరింది. కుందేలు దానిని ఒక లోతైన బావి దగ్గరకు తీసుకెళ్లింది. సింహం బావిలో తన నీడను చూసి, అది మరొక సింహం అనుకుని బావిలోకి దూకి ప్రాణాలు కోల్పోయింది. కుందేలు తన తెలివితేటలతో అడవిని కాపాడింది."""

# Voice options (Assuming 'male' and 'female' based on readme.md examples)
# Refer to Sarvam AI documentation for available voice IDs/names
MALE_VOICE = "shubh" # Placeholder, e.g., 'arvind' or a specific ID
FEMALE_VOICE = "shreya" # Placeholder, e.g., 'vini' or a specific ID

# Output directory for audio files
OUTPUT_DIR = "outputs"

def generate_audio(text: str, voice_name: str, output_filename: str):
    """
    Generates audio from text using the Sarvam AI TTS API and saves it to a file.

    Args:
        text: The text to convert to speech.
        voice_name: The name or ID of the voice to use.
        output_filename: The name of the file to save the audio to (e.g., "story_male.wav").
    """
    if not SARVAM_API_KEY or SARVAM_API_KEY == "YOUR_SARVAM_API_KEY":
        print("Error: Sarvam AI API Key is not set. Please update SARVAM_API_KEY in the script.")
        return
    # Check if the API endpoint is the placeholder and warn if it is
    if SARVAM_API_ENDPOINT == "https://api.sarvam.ai/tts/v1/synthesize" or SARVAM_API_ENDPOINT == "https://api.sarvam.ai/text-to-speech":
        print("Warning: Sarvam AI API Endpoint might be a placeholder. Ensure it is correctly set.")

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "voice": voice_name,
        "language": "te",  # Assuming Telugu language code
    }

    try:
        print(f"Requesting audio for voice: {voice_name}...")
        response = requests.post(SARVAM_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        
        # Expected format: {"audios": ["base64_encoded_audio_string"]}
        if 'audios' in data and isinstance(data['audios'], list) and len(data['audios']) > 0:
            audio_base64 = data['audios'][0]
            audio_bytes = base64.b64decode(audio_base64)

            os.makedirs(OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            print(f"Successfully generated audio: {output_path}")
        else:
            print(f"Error: Unexpected API response format for voice {voice_name}.")
            print(f"Response JSON: {data}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error generating audio for voice {voice_name}: {e}")
        try:
            error_details = response.json()
            print(f"Error Details: {error_details}")
        except requests.exceptions.JSONDecodeError:
            print(f"Response Text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
    except base64.binascii.Error as e:
        print(f"Base64 decoding error for voice {voice_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Starting audio generation for the story...")

    # Generate audio for the male voice
    generate_audio(STORY_TEXT, MALE_VOICE, "story_male.wav")
    generate_audio(STORY_TEXT, MALE_VOICE, "story_male_new.wav")

    # Generate audio for the female voice
    generate_audio(STORY_TEXT, FEMALE_VOICE, "story_female.wav")
    generate_audio(STORY_TEXT, FEMALE_VOICE, "story_female_new.wav")

    print("Audio generation process completed.")
