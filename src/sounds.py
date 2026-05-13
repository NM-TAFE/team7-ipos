import numpy as np
import pyaudio

# Code derived from: https://www.py4u.org/blog/python-realtime-audio-streaming-with-pyaudio-or-something-else/
def play_sound(current_player):
    """
    Use this to have the program play a simple sound.
    :param current_player: changes which pitch is played if != 'X'
    :return: generates a sound
    """
    # Audio parametres
    sample_rate = 44100 # Hz
    tone_duration = 0.456 # Seconds
    if current_player == 'X':
        tone_frequency = 440 # Hz (A4)
    else:
        tone_frequency = 523.25 # Hz (C4)

    t = np.linspace(0, tone_duration, int(sample_rate * tone_duration), endpoint=False)

    # Generate sine wave: y = A * sin(2πft)
    amplitude = 0.2 #Reduce volume (0.0 to (1.0)
    sine_wave = amplitude * np.sin(2 * np.pi * tone_frequency * t)

    # Normalise to 16-bit range and convert to into16
    sine_wave_int16 = (sine_wave * 32767).astype(np.int16)

    # Initialise PyAudio
    p = pyaudio.PyAudio()

    # Open output stream
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        output=True
    )

    # Play the audio
    stream.write(sine_wave_int16.tobytes())

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

