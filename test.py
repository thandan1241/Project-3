from elevenlabs.client import ElevenLabs
import os
from dotenv import load_dotenv
load_dotenv()
client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")
)

audio = client.text_to_speech.convert(
    text="Hello everyone, and welcome to this tutorial. Today, we are going to explore how artificial intelligence can help you create high-quality videos automatically, from converting text into natural-sounding speech, to combining visuals, audio, and structured content into a complete and professional final product. This process not only saves you a significant amount of time, but also allows you to focus more on creativity and storytelling, making your videos more engaging and effective for your audience.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Lưu file
with open("voice.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("Saved as voice.mp3")