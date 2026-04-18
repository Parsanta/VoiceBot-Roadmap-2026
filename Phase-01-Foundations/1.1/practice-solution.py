import os, sounddevice as sd, numpy as np, wave, tempfile, time
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
    latencies = {"record": [], "transcribe": [], "think": [], "speak": []}
    iteration = 0
    
    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        
        # Record
        t0 = time.perf_counter()
        wav = record()
        t_record = time.perf_counter() - t0
        latencies["record"].append(t_record)
        print(f"RECORD: {t_record:.3f}s")
        
        # Transcribe
        t0 = time.perf_counter()
        user_text = transcribe(wav)
        t_transcribe = time.perf_counter() - t0
        latencies["transcribe"].append(t_transcribe)
        print(f"USER: {user_text}")
        print(f"TRANSCRIBE: {t_transcribe:.3f}s")
        
        # Check for exit condition
        if user_text.lower().strip() == "goodbye":
            print("\nGoodbye!")
            break
        
        # Think
        t0 = time.perf_counter()
        reply = think(user_text)
        t_think = time.perf_counter() - t0
        latencies["think"].append(t_think)
        print(f"BOT: {reply}")
        print(f"THINK: {t_think:.3f}s")
        
        # Speak
        t0 = time.perf_counter()
        speak(reply)
        t_speak = time.perf_counter() - t0
        latencies["speak"].append(t_speak)
        print(f"SPEAK: {t_speak:.3f}s")
    
    # Print summary
    print("\n" + "="*50)
    print("LATENCY ANALYSIS")
    print("="*50)
    for stage, times in latencies.items():
        if times:
            avg = sum(times) / len(times)
            max_time = max(times)
            print(f"{stage.upper():12} avg={avg:.3f}s  max={max_time:.3f}s  n={len(times)}")
    
    total_times = {stage: sum(times) for stage, times in latencies.items()}
    total_sum = sum(total_times.values())
    print("\nBOTTLENECK ANALYSIS (% of total time):")
    for stage, total_time in sorted(total_times.items(), key=lambda x: x[1], reverse=True):
        if total_sum > 0:
            percentage = (total_time / total_sum) * 100
            print(f"{stage.upper():12} {percentage:6.1f}%")