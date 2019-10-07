import pyaudio
import wave
import sys


def receive(input_audio):


    pya = pyaudio.PyAudio()
    OUTPUT_SAMPLE_RATE = 44100
    stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=OUTPUT_SAMPLE_RATE, output=True)

    bytestream = input_audio
    stream.write(bytestream)
    stream.stop_stream()
    stream.close()