import json
import subprocess
import time
import wave
import pyaudio
import threading
from pynput import keyboard
from pynput.keyboard import Key
import requests


SEND_URI = "http://192.168.106.220:8000/reserve-spell"
process = None

def whisper_runner(filename):
    global process
    while True:
        print("start whisper")
        # ここに音声認識の処理を書く
        process = subprocess.Popen(["./whisper/whisper.cpp/main",
            "-t", "9",
            "-f", "output.wav",
            "-m", "./whisper/whisper.cpp/models/ggml-large.bin",
            "-l", "ja", "--output-json",
            "--output-file", "text", "--prompt", "竜神 慈悲 轟け"], stdin=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL,
                                   text=True)

        process.wait()
        print("finish whisper")

        whisper_response = json.load(open("text.json", "r", encoding="utf-8"))

        try:
            whisper_text = whisper_response["transcription"][0]["text"]
            print(f"whisper_text: \"{whisper_text}\"")
        except IndexError:
            print("failed to get whisper_text")
            continue

        try:
            requests.post(SEND_URI, json={"text": whisper_text.replace(" ", "")})
        except:
            print("failed to post")
        finally:
            print("finish post")



# 録音関数
def record_audio(filename):
    global recording
    global process
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
                device_info = p.get_device_info_by_index(i)
                print(f'Default Sample Rate: {device_info["defaultSampleRate"]}')
                print(f'Max Input Channels: {device_info}')
                device_index = int(i)
                break
    if device_index == -1:
        print("not found OpenComm2")
        exit(1)

    frames_per_buffer = 1024
    print(device_index)

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=frames_per_buffer)

    while True:
        while not recording:
            _ = stream.read(frames_per_buffer)

        frames = []

        print("Recording... Press and hold 'r' to stop recording")

        while recording:
            data = stream.read(frames_per_buffer)
            frames.append(data)

        print("Stopped recording.")


        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
        wf.close()

        print("Saved recording.")

        process.stdin.write("\n")
        process.stdin.flush()
    stream.stop_stream()
    stream.close()

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
    threading.Thread(target=whisper_runner, args=('output.wav',)).start()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
