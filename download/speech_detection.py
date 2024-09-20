import os
from typing import List
import concurrent.futures
import torchaudio
from speechbrain.inference import EncoderClassifier
import logging



class Detect:
    def __init__(self):
        self.language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa",
                                                          savedir="speech_video_controller/tmp")

    def detect_language(self, audio_path: str) -> str:
        try:
            signal, sample_rate = torchaudio.load(audio_path)

            if signal.shape[0] > 1:
                signal = signal.mean(dim=0, keepdim=True)

            if sample_rate != 16000:
                signal = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(signal)

            prediction = self.language_id.classify_batch(signal)
            predicted_language = prediction[3][0]

            return predicted_language

        except Exception as detect_error:
            logging.error(f"Detection Error -> {detect_error}")
            return ""

    def detect_languages(self, mp3_paths: List[str]) -> dict:
        audio_paths = [mp3_path for mp3_path in mp3_paths]
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(self.detect_language, audio_path):
                           mp3_path for audio_path, mp3_path in zip(audio_paths, mp3_paths)}
            detected_languages_dict = {}

            for future in concurrent.futures.as_completed(futures):
                mp3_path = futures[future]
                detected_language = future.result()
                detected_languages_dict[mp3_path] = detected_language

            return detected_languages_dict

    @staticmethod
    def get_azerbaijani_sounds(detected_languages_dict: dict) -> List[str]:
        azerbaijani_ids = [mp3_path for mp3_path, language in detected_languages_dict.items()
                           if language == "az: Azerbaijani"]
        return azerbaijani_ids

    @staticmethod
    def delete_non_azerbaijani_sounds(detected_languages_dict: dict, postgres):
        non_azerbaijani_ids = [mp3_path for mp3_path, language in detected_languages_dict.items()
                               if language != "az: Azerbaijani"]
        for mp3_path in non_azerbaijani_ids:
            audio_path = mp3_path
            if os.path.exists(audio_path):
                try:
                    postgres.delete_post(audio_path)
                    os.remove(audio_path)
                    logging.info(f"Fayl silindi: {audio_path}")
                except Exception as e:
                    logging.error(f"Fayl silinmədi: {audio_path}, Error: {e}")


def detection(mp3_paths: List[str], postgres) -> List[str]:
    detect_instance = Detect()
    detected_languages = detect_instance.detect_languages(mp3_paths)
    azerbaijani_ids = Detect.get_azerbaijani_sounds(detected_languages)

    detect_instance.delete_non_azerbaijani_sounds(detected_languages, postgres)

    logging.info("Audio Languages Successfully Detected")
    return azerbaijani_ids


async def main_detect(postgres):
    mp3_paths = postgres.get_url_for_content()
    from pathlib import Path
    os.chdir(Path(__file__).resolve().parent.parent)
    azerbaijani_mp3_paths = detection(mp3_paths, postgres)
    return


