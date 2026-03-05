import os
import io
import base64
import requests
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

# --- Configuration ---
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "your_actual_key_here") 
SARVAM_API_ENDPOINT = "https://api.sarvam.ai/text-to-speech" 

# Story Text
STORY_TEXT = """ఒక దట్టమైన అడవిలో ఒక బలమైన సింహం ఉండేది. అది ప్రతిరోజూ అడవిలోని జంతువులను వేటాడేది. ఒకరోజు ఒక చిన్న కుందేలు వంతు వచ్చింది. ఆ కుందేలు చాలా తెలివైనది. అది సింహం దగ్గరకు ఆలస్యంగా వెళ్లింది. సింహం కోపంగా ఎందుకు ఆలస్యమైందని అడిగింది. అప్పుడు కుందేలు, "రాజా, దారిలో నాకు మరొక సింహం కనిపించింది, అది మిమ్మల్ని సవాలు చేస్తోంది" అని చెప్పింది. సింహం ఆవేశంతో కుందేలును ఆ మరొక సింహం దగ్గరకు తీసుకెళ్లమని కోరింది. కుందేలు దానిని ఒక లోతైన బావి దగ్గరకు తీసుకెళ్లింది. సింహం బావిలో తన నీడను చూసి, అది మరొక సింహం అనుకుని బావిలోకి దూకి ప్రాణాలు కోల్పోయింది. కుందేలు తన తెలివితేటలతో అడవిని కాపాడింది."""

# Updated Voice Selections for bulbul:v3
MALE_VOICE = "shubh" 
FEMALE_VOICE = "priya"
OUTPUT_DIR = "outputs"
MAX_CHUNK_SIZE = 500  # bulbul:v3 handles up to 2500, but smaller chunks are safer for memory

def split_text_into_chunks(text, chunk_size):
    """Splits text gracefully at sentence boundaries."""
    # Your original logic was good; keeping it as is for your learning
    import re
    sentences = re.split('(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def generate_audio(text_chunks, voice_name, output_filename):
    """Hits the API for each chunk and stitches them together."""
    # Correct Headers per documentation
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    all_audio_segments = []
    
    for i, chunk in enumerate(text_chunks):
        # Correct Payload keys
        payload = {
            "text": chunk,
            "target_language_code": "te-IN",
            "speaker": voice_name,
            "model": "bulbul:v3"
        }

        try:
            print(f"🎙️ Processing {voice_name}: Chunk {i+1}/{len(text_chunks)}...")
            if not SARVAM_API_KEY or SARVAM_API_KEY == "your_actual_key_here":
                print("❌ Error: API Key is not set correctly. Please check your .env file.")
                return

            response = requests.post(SARVAM_API_ENDPOINT, headers=headers, json=payload)
            
            if response.status_code != 200:
                print(f"❌ Error on chunk {i+1}: {response.status_code} - {response.text}")
                continue

            data = response.json()
            if 'audios' in data and data['audios']:
                audio_bytes = base64.b64decode(data['audios'][0])
                segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
                all_audio_segments.append(segment)
            else:
                print(f"⚠️ Warning: No audio data in response for chunk {i+1}")
            
        except Exception as e:
            print(f"❌ Unexpected error on chunk {i+1}: {e}")

    if all_audio_segments:
        combined = sum(all_audio_segments)
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        combined.export(output_path, format="wav")
        print(f"✅ Saved: {output_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Chunking
    chunks = split_text_into_chunks(STORY_TEXT, MAX_CHUNK_SIZE)
    print(f"Starting sprint: {len(chunks)} chunks found.")

    # 2. Execution
    generate_audio(chunks, MALE_VOICE, "story_male")
    generate_audio(chunks, MALE_VOICE, "story_male_new")
    generate_audio(chunks, FEMALE_VOICE, "story_female")
    generate_audio(chunks, FEMALE_VOICE, "story_female_new")
    
    print("🚀 Project Complete. Check the 'outputs' folder.")
