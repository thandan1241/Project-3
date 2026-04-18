import os
import json
import re
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import hashlib

load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")

# ====== CACHE MANAGER ======
CACHE_FILE = "voice_cache.json"
OUTPUT_FOLDER = "video1"  # Change to "video2" to generate Video 2
VIDEO_VERSION = 1  # 1 for V1, 2 for V2

# Determine output folder based on VIDEO_VERSION
if VIDEO_VERSION == 2:
    OUTPUT_FOLDER = "video2"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def load_cache():
    """Load voice cache from file"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save voice cache to file"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_text_hash(text):
    """Generate hash from text for cache key"""
    return hashlib.md5(text.encode()).hexdigest()

def get_cached_filename(text_hash):
    """Get filename from cache or None if not cached"""
    cache = load_cache()
    key = f"{text_hash}"
    if key in cache:
        return cache[key]["filename"]
    return None

def cache_voice(text_hash, text, filename):
    """Cache voice file info"""
    cache = load_cache()
    cache[text_hash] = {
        "text_preview": text[:100],
        "filename": filename
    }
    save_cache(cache)

def parse_markdown(file_path):
    """Parse markdown file and extract scripts with names"""
    scripts = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern to match [V1 | ...] or [V2 | ...] followed by text until next [...] or end of file
    pattern = r'\[V[12] \| ([^\]]+)\]\s*\n(.*?)(?=\n\[V[12] \||$)'
    
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        name = match.group(1).strip()
        text = match.group(2).strip()
        
        if text:  # Only add if text is not empty
            scripts.append({
                "name": name,
                "text": text
            })
    
    return scripts

# ====== MAIN EXECUTION ======
print("Parsing markdown file...")
scripts = parse_markdown("script2.md")

print(f"Found {len(scripts)} scripts\n")

client = ElevenLabs(api_key=API_KEY)

total_scripts = len(scripts)
skipped = 0
generated = 0

for i, script_data in enumerate(scripts, 1):
    script_name = script_data["name"]
    script_text = script_data["text"]
    text_hash = get_text_hash(script_text)
      # Clean filename (remove invalid characters for Windows)
    clean_name = script_name.replace("/", "-").replace("\\", "-").replace(":", "-").replace("?", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace("|", "-").replace('"', "-")
    filename = os.path.join(OUTPUT_FOLDER, f"{clean_name}.mp3")
      # Check cache first
    cached_file = get_cached_filename(text_hash)
    if cached_file and os.path.exists(cached_file):
        print(f"[{i}/{total_scripts}] [CACHE] {script_name}")
        skipped += 1
        continue
    
    print(f"[{i}/{total_scripts}] [GENERATING] {script_name}...")
    
    try:
        audio = client.text_to_speech.convert(
            text=script_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        
        # Convert stream to bytes
        audio_bytes = b"".join(audio)
        
        # Save file
        with open(filename, "wb") as f:
            f.write(audio_bytes)
        
        # Cache the file info
        cache_voice(text_hash, script_text, filename)
        
        print(f"[OK] Saved {filename}")
        generated += 1
    except Exception as e:
        print(f"[ERROR] Failed to generate {script_name}: {str(e)}")

print(f"\n=== SUMMARY ===")
print(f"Total scripts: {total_scripts}")
print(f"Generated: {generated}")
print(f"From cache: {skipped}")
print(f"Output folder: {OUTPUT_FOLDER}")
print(f"DONE!")
