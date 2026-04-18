import os, sounddevice as sd, numpy as np, wave, tempfile
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def record(seconds=4, sr=16000):
    print("Speak now...")
    audio = sd.rec(int(seconds*sr), samplerate=sr, channels=1, dtype="int16")
    sd.wait()
    path = tempfile.mktemp(suffix=".wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(audio.tobytes())
    return path

def transcribe(path):
    with open(path,"rb") as f:
        return client.audio.transcriptions.create(model="whisper-1", file=f).text

def think(text):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"Reply in ≤ 20 words."},
                  {"role":"user","content":text}])
    return r.choices[0].message.content

def speak(text):
    resp = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    out = tempfile.mktemp(suffix=".mp3"); resp.stream_to_file(out)
    os.system(f"ffplay -autoexit -nodisp {out}")  

if __name__ == "__main__":
    wav = record()
    user_text = transcribe(wav); print("USER:", user_text)
    reply = think(user_text);    print("BOT :", reply)
    speak(reply)