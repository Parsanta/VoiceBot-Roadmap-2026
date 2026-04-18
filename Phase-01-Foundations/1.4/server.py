from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/audio")
async def audio_ws(ws: WebSocket):
    await ws.accept()
    print("Client connected")
    try:
        while True:
            chunk = await ws.receive_bytes()        # receive 20ms of audio
            print(f"Server got: {len(chunk)} bytes")
            await ws.send_bytes(chunk)              # echo back
    except Exception as e:
        print(f"Disconnected: {e}")
        await ws.close()