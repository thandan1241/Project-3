import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")
# ====== TEXT ======
script = """
Welcome to this tutorial on Flow Matching.
In this video, we will explore the basic concepts, advanced designs,
and real-world applications of flow-based generative models.
"""

# ====== GENERATE VOICE ======
print("Generating voice...")

client = ElevenLabs(api_key=API_KEY)

audio = client.text_to_speech.convert(
    text=script,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Convert stream to bytes
audio_bytes = b"".join(audio)

# Save file
with open("voice.mp3", "wb") as f:
    f.write(audio_bytes)

print("DONE! File saved as voice.mp3")