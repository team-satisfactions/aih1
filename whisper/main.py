import json
import subprocess
import time
import wave
import pyaudio
import threading
from pynput import keyboard
from pynput.keyboard import Key
import requests


SEND_URI = "http://192.168.106.214:8000/receive-spell"


# 録音関数
def record_audio(filename):
    global recording
    print("start record thread")

    p = pyaudio.PyAudio()

    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    device_index = -1
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            name = p.get_device_info_by_host_api_device_index(0, i).get('name')
            print("Input Device id ", i, " - ", name)
            if name.startswith("OpenComm2"):
                print("found OpenComm2")
                device_index = int(i)
                break
    if device_index == -1:
        print("not found OpenComm2")
        exit(1)

    print(device_index)
    while True:
        while not recording:
            time.sleep(0.001)

        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=1024)

        frames = []

        print("Recording... Press and hold 'r' to stop recording")

        while recording:
            data = stream.read(1024)
            frames.append(data)

        print("Stopped recording.")

        stream.stop_stream()
        stream.close()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("start whisper")
        # ここに音声認識の処理を書く
        subprocess.run([
            "./whisper/whisper.cpp/main",
            "-t", "9",
            "-f", "output.wav",
            "-m", "./whisper/whisper.cpp/models/ggml-large.bin",
            "-l", "ja", "--output-json",
            "--output-file", "text"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("finish whisper")
        whisper_response = json.load(open("text.json", "r", encoding="utf-8"))

        whisper_text = whisper_response["transcription"][0]["text"]
        print(f"whisper_text: \"{whisper_text}\"")

        requests.post(SEND_URI, json={"text": whisper_text.replace(" ", "")})
        print("finish post")


# キーが押されている間録音するフラグ
recording = False

def on_press(key):
    global recording
    if key == Key.space:
        recording = True

def on_release(key):
    global recording
    if key == Key.space:
        recording = False


if __name__ == '__main__':
    # キーボードリスナーをセットアップ
    threading.Thread(target=record_audio, args=('output.wav',)).start()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
