import whisper
import os

def transcribe_audio_files(paths):
    model = whisper.load_model("base")
    transcriptions = []

    for path in paths:
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".mp3") or filename.endswith(".wav"):
                    file_path = os.path.join(path, filename)
                    transcriptions.append(transcribe_single_file(model, file_path))
        elif os.path.isfile(path) and (path.endswith(".mp3") or path.endswith(".wav")):
            transcriptions.append(transcribe_single_file(model, path))
        else:
            print(f"Skipping unsupported file or directory: {path}")

    return transcriptions

def transcribe_single_file(model, file_path):
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    print(f"Detected language for {file_path}: {detected_language}")

    options = whisper.DecodingOptions(language=detected_language)
    result = model.decode(mel, options)

    return result.text

paths = [
    "/Users/macbook/Desktop/HarayFacebookApp/resource/video_185da43d-fa91-4f7f-bcf8-482ea8127c41.mp3",
    "/Users/macbook/Desktop/HarayFacebookApp/resource/video_136aa6d4-1d5c-4210-bd90-996d853aacc8.mp3"
]
transcriptions = transcribe_audio_files(paths)
for transcription in transcriptions:
    print(transcription)
