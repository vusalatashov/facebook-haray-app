import whisper
import os

def transcribe_audio_files_from_directory(directory_path):
    model = whisper.load_model("base")
    transcriptions = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                file_path = os.path.join(root, filename)
                audio = whisper.load_audio(file_path)
                audio = whisper.pad_or_trim(audio)
                mel = whisper.log_mel_spectrogram(audio).to(model.device)

                _, probs = model.detect_language(mel)
                detected_language = max(probs, key=probs.get)
                print(f"Detected language for {file_path}: {detected_language}")

                if detected_language == 'az':
                    transcriptions.append(transcribe_single_file(model, file_path))

    return transcriptions

def transcribe_single_file(model, file_path):
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    options = whisper.DecodingOptions(language='az')
    result = model.decode(mel, options)

    return result.text


directory_path = "/Users/macbook/Desktop/HarayFacebookApp/resource/"
transcriptions = transcribe_audio_files_from_directory(directory_path)
for transcription in transcriptions:
    print(transcription)