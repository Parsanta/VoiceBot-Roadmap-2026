A voice bot is a pipeline that converts spoken audio into spoken audio, with a brain in the middle. At production scale, five stages run concurrently:

- Audio capture — microphone or telephony stream (8 kHz µ-law for phones, 16/24/48 kHz PCM on web).
- VAD (Voice Activity Detection) — decides when the user started and stopped speaking.
- ASR / STT (Automatic Speech Recognition) — turns audio into text (Whisper, Deepgram, Google STT).
- NLU + LLM — the "brain" interprets intent, calls tools, and generates a reply (GPT-4, Claude, Gemini).
- TTS (Text-to-Speech) — turns the reply back into audio (ElevenLabs, Azure, Coqui).
Older systems had a separate NLU layer (intent + slot models like Rasa/Dialogflow) Modern stacks collapse NLU into the LLM. The latency target for a natural-feeling call is <500 ms from end-of-user-speech to first audio byte of the response which is why every stage must stream rather than block.

Industry context: Duolingo Max, Klarna's voice support, Meta's Ray-Ban glasses, and customer-service deflection at any Fortune 500 call center all run this exact pipeline. The difference between a $10M company and a failed demo is usually latency and interruption handling, not the model.