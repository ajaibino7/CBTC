import os
import sounddevice as sd
import wavio
import numpy as np
from pynput import keyboard

        
fs = 44100  
channels = 1  
dtype = 'int16'  

        
recording_chunks = []

        
output_directory = "recordings"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

        
def callback(indata, frames, time, status):
    recording_chunks.append(indata.copy())

        
stream = sd.InputStream(samplerate=fs, channels=channels, dtype=dtype, callback=callback)

        
recording = True

def on_press(key):
    global recording
    if key == keyboard.Key.esc:  
        recording = False
        return False  

        
with stream:
    print("Recording... Press 'esc' to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        while recording:
            pass
        listener.join()
print("Recording stopped")

        
recording = np.concatenate(recording_chunks, axis=0)

        
filename = input("Enter the file name with '.wav' extension: \n")
save_path = os.path.join(output_directory, filename)

        
wavio.write(save_path, recording, fs, sampwidth=2)
print(f"Recording saved as {filename}")

