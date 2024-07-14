import os
import sounddevice as sd
import wavio
import numpy as np
from pynput import keyboard

        # Set the parameters
fs = 44100  
channels = 1  
dtype = 'int16'  

        # Create an empty list to store the recording chunks
recording_chunks = []

        # Define the directory where you want to save the recordings
output_directory = "recordings"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

        # Define a callback function to continuously record audio chunks
def callback(indata, frames, time, status):
    recording_chunks.append(indata.copy())

        # Create an InputStream with the callback function
stream = sd.InputStream(samplerate=fs, channels=channels, dtype=dtype, callback=callback)

        # Flag to control the recording loop
recording = True

def on_press(key):
    global recording
    if key == keyboard.Key.esc:  # Use the 'esc' key to stop recording
        recording = False
        return False  

        # Start the stream
with stream:
    print("Recording... Press 'esc' to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        while recording:
            pass
        listener.join()
print("Recording stopped")

        # Concatenate all recorded chunks into a single numpy array
recording = np.concatenate(recording_chunks, axis=0)

        # Define the filename and save path
filename = input("Enter the file name with '.wav' extension: \n")
save_path = os.path.join(output_directory, filename)

        # Save the recording to a file
wavio.write(save_path, recording, fs, sampwidth=2)
print(f"Recording saved as {filename}")

