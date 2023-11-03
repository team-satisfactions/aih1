import json
import subprocess
import time
import wave
import pyaudio
import threading
from pynput import keyboard
from pynput.keyboard import Key
import requests


def on_press(key):
    global recording
    print(key)
    if key == Key.space:
        recording = True

def on_release(key):
    global recording
    if key == Key.space:
        recording = False


if __name__ == '__main__':
    # キーボードリスナーをセットアップ
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()