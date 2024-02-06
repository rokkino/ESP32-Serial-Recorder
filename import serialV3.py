from pydub import AudioSegment #pip install pydub
import serial                  #python.exe -m pip install --upgrade pip
import wave
import time
import os


def next_file_number(folder_path, base_name):
    counter = 1
    while True:
        file_path = os.path.join(folder_path, f"{base_name}_{counter}.wav")
        if not os.path.exists(file_path):
            return counter
        counter += 1

# Path to save the wave file
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Windows
folder_path = os.path.join(desktop, 'Recording_AI')
os.makedirs(folder_path, exist_ok=True)

# Serial port configuration
ser = serial.Serial('COM6', 500000)  # Update COM port as needed

# Constants for recording
sample_rate = 25000  # in Hertz
sample_width = 2  # in bytes (16 bits)
record_seconds = 2  # duration of recording
total_samples = sample_rate * record_seconds

# Number of recordings
num_recordings = 1  # Change this to set how many recordings you want

# Path to save the wave file
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Windows
folder_path = os.path.join(desktop, 'Recording_AI')
os.makedirs(folder_path, exist_ok=True)

for recording in range(num_recordings):
    file_number = next_file_number(folder_path, 'output')
    file_path = os.path.join(folder_path, f'output_{file_number}.wav')

    print(f"Recording {recording + 1} now!\n\n")
    for second in range(record_seconds, 0, -1):
        print(f"second {second}, Rec {recording + 1} ")
        time.sleep(1)

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(sample_width)  # 16 bits per sample
        wf.setframerate(sample_rate)  # Set the sample rate

        data = ser.read(total_samples * sample_width)
        wf.writeframes(data)

    # Remove the first 0.3 seconds
    audio = AudioSegment.from_file(file_path)
    trimmed_audio = audio[300:]  # Trim first 300ms
    trimmed_audio.export(file_path, format="wav")

    print(f"Recording {recording + 1} finished. File saved at: {file_path}")

ser.close()
