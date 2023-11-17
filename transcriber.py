import os
import csv
import speech_recognition as sr

def transcribe_audio_files_in_directory(directory_path, csv_file_path, bad_audio_directory):
    r = sr.Recognizer()

    # Create the bad audio directory if it doesn't exist
    os.makedirs(bad_audio_directory, exist_ok=True)

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        
        for filename in os.listdir(directory_path):
            if filename.endswith(".wav"):
                file_path = os.path.join(directory_path, filename)
                
                with sr.AudioFile(file_path) as source:
                    audio = r.record(source)
                    try:
                        # Transcribe
                        transcription = r.recognize_google(audio)
                        writer.writerow([filename, transcription, transcription])
                    except sr.UnknownValueError:
                        print(f"Google Web Speech API could not understand audio for file: {filename}. Moving it to badAudio directory.")
                        # Move the bad audio file to the badAudio directory
                        os.rename(file_path, os.path.join(bad_audio_directory, filename))
                    except sr.RequestError as e:
                        print("Could not request results from Google Web Speech API service; {0}".format(e))

# Usage
transcribe_audio_files_in_directory('/home/eleven/coquii/WORKFROMHERE/wavs', '/home/eleven/coquii/WORKFROMHERE/metadata.csv', '/home/eleven/coquii/WORKFROMHERE/badAudio')
