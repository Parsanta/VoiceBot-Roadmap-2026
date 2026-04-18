# REST APIs & WebSockets (streaming voice)

Voice pipelines live or die on their transport layer.

- REST is request/response. Good for one-shot transcription of a recorded file, configuration, and non-streaming TTS. Every request pays a TLS + TCP round-trip.
- Server-Sent Events (SSE) is unidirectional server→client streaming. LLM token streaming often uses SSE.
- WebSockets are bidirectional, full-duplex, low-latency. This is what Deepgram, OpenAI Realtime, Twilio Media Streams, ElevenLabs streaming, LiveKit, and Pipecat all use under the hood.
- WebRTC sits on top of UDP with DTLS/SRTP, does NAT traversal, congestion control, and jitter buffering. Perfect for browser-to-bot real-time, harder to self-host.

For voice agents, you'll write and consume websocket servers constantly. Master them.