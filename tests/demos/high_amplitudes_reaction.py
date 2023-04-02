##############################################################
# Zakhar-the-Robot - Auditory Toolkit, Nikita Mortuzaiev, 2022
##############################################################

import time
from tkinter import NW, Tk, Canvas

import numpy as np
from brian2 import Hz, kHz, second
from brian2hears import dB_type, Sound
from PIL import ImageTk, Image

from brain_pycore.zmq import ZmqPublisherThread, ZmqSubscriberThread
from src.auditory_toolkit.casa.cochleagram import cochlea
from src.auditory_toolkit.filterbanks.time_frequency import ThresholdFilterbank

from images import *

address = "localhost"
port = 12345
topic = "HighAmplitudesDemo"

tk = Tk()
canvas = Canvas(tk, width=336, height=256)
canvas.pack()

samplerate = 8*kHz
segment_duration = 2*second
n_channels = 1  # Change to 2 if you want to play the sound

noise = Sound.whitenoise(segment_duration, samplerate=samplerate, nchannels=n_channels).atlevel(dB_type(70))
tone = Sound.tone(440*Hz, segment_duration, nchannels=n_channels).atlevel(dB_type(70))

sound = Sound.sequence([tone, noise] * 10)
# sound.play(sleep=True)

cochleagram, center_freqs = cochlea(sound, n_channels=64, min_freq=20*Hz, max_freq=20*kHz, return_cf=True)
filterbank = ThresholdFilterbank(cochleagram, threshold=0.25)

samples_fetched = 0

faces = {
    "angry": ImageTk.PhotoImage(Image.open(ANGRY_JPG)),
    "blink": ImageTk.PhotoImage(Image.open(BLINK_JPG)),
    "calm": ImageTk.PhotoImage(Image.open(CALM_JPG)),
    "happy": ImageTk.PhotoImage(Image.open(HAPPY_JPG)),
    "sad": ImageTk.PhotoImage(Image.open(SAD_JPG)),
}
current_face = faces["calm"]


def publisher_callback():
    global samples_fetched
    to_fetch = 8000
    buffer = filterbank.buffer_fetch(samples_fetched, samples_fetched + to_fetch)
    samples_fetched += to_fetch

    freqs_info = buffer.any(axis=0).astype(int)
    freqs_info_str = "".join(freqs_info.astype(str))

    cf = center_freqs[np.where(freqs_info)[0]][0] if freqs_info.sum() > 0 else None

    print(f"Buffer shape: {buffer.shape}, "
          f"buffer start: {filterbank.cached_buffer_start / filterbank.samplerate}, "
          f"first freq: {cf}, threshold exceeded: {freqs_info_str}")

    return freqs_info_str


def subscriber_callback(msg):
    global current_face
    data = msg.split(" ", maxsplit=1)
    channels_exceeded = sum([int(c) for c in data])

    if channels_exceeded > 5:
        print("Changing expression to \"angry\"")
        current_face = faces["angry"]
        time.sleep(1)
    elif channels_exceeded > 0:
        print("Changing expression to \"sad\"")
        current_face = faces["sad"]
        time.sleep(1)

    current_face = faces["calm"]
    time.sleep(1)


if __name__ == "__main__":

    pub = ZmqPublisherThread(port, topic, publisher_callback, publishing_freq_hz=1)
    sub = ZmqSubscriberThread(port, topic, subscriber_callback, address)

    pub.start()
    sub.start()

    try:
        while True:
            canvas.create_image(0, 0, anchor=NW, image=current_face)
            tk.update_idletasks()
            tk.update()
    except KeyboardInterrupt:
        pass
    finally:
        pub.stop()
        sub.stop()
