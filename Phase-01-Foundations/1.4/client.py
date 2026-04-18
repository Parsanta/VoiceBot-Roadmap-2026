import asyncio, websockets, sounddevice as sd, numpy as np, queue

q = queue.Queue()

def cb(indata, *_):
    q.put(bytes(indata))
    print(f"Mic chunk: {len(indata)} bytes")    # confirm mic is working

async def main():
    print("Connecting to server...")
    async with websockets.connect("ws://localhost:8000/audio") as ws:
        print("Connected! Speak into your mic...")
        with sd.RawInputStream(samplerate=16000, blocksize=320,
                               dtype="int16", channels=1, callback=cb):
            while True:
                await ws.send(q.get())
                try:
                    reply = await asyncio.wait_for(ws.recv(), timeout=0.01)
                    audio = np.frombuffer(reply, dtype=np.int16)
                    sd.play(audio, samplerate=16000)
                    print(f"Playing back: {len(reply)} bytes")
                except asyncio.TimeoutError:
                    pass  

asyncio.run(main())