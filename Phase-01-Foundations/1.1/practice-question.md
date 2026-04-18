# MINI_PROJECT
Extend the script above to loop continuously record, transcribe, reply, speak, repeat until the user says "goodbye". Measure and print the latency of each stage with time.perf_counter(). Where is the bottleneck?

# Theoretical Questions
1) Why is 8 kHz µ-law used on phone calls but 16/24 kHz PCM on the web?
2) Sketch the data-flow diagram of an end-to-end voice bot and label each stage's typical latency.
3) If the user interrupts the bot mid-sentence, which components must know about it?