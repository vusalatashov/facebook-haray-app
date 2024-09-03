import asyncio
import concurrent.futures
import base64
import logging
import os
import aiohttp
from pydub import AudioSegment
from config.config import ROOT_DIR
from database.postgres_video import PostgresVideo

os.chdir(ROOT_DIR)

class Transcribe:
    async def transcribe_multiple_audios(self, domain: str, base_64_audios: list, postgres, mp3_paths: list) -> list:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(
                    self.transcribe_audio(session, domain, base64_audio, postgres, mp3_path)
                )
                for base64_audio, mp3_path in zip(base_64_audios, mp3_paths)
                if self.is_short_audio(mp3_path)
            ]

            results = []
            for task in tasks:
                result = await task
                results.append(result)
                logging.info(f"Transcription completed for one audio file with result: {result}")

            return results

    def is_short_audio(self, file_path: str) -> bool:
        try:
            audio = AudioSegment.from_file(file_path, format="ogg")
            duration = len(audio) / 1000  # Süreyi saniye cinsinden almak için 1000'e bölün
            return duration < 600  # 1 dakikadan kısa mı?
        except Exception as e:
            logging.error(f"Failed to open audio file {file_path}: {e}")
            return False

    async def transcribe_audio(self, session: aiohttp.ClientSession, domain: str, base_64_audio: str, postgres, mp3_path: str, ext: str = ".ogg") -> str:
        try:
            url = f"http://{domain}:1941/stt"
            data = {
                "voice": base_64_audio,
                "mp3_path": mp3_path
            }

            async with session.post(url, json=data) as response:
                result = await response.json()

                logging.info(f"Response for audio at {mp3_path}: {result}")

                text = result.get("result", {}).get("transcribed_text", "No transcribed text available")

                postgres.update_conversion_status(mp3_path, text)

                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                    logging.info(f"File {mp3_path} removed successfully.")
                else:
                    logging.warning(f"File {mp3_path} not found.")

                return text
        except Exception as error:
            logging.error(f"Error during transcription for {mp3_path}: {error}")
            return ""

class Base64:
    def convert_file_to_base64(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            logging.error(f"Failed to convert {file_path} to base64: {e}")
            return ""

    def get_base64_conversions(self, mp3_paths: list) -> list:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(self.convert_file_to_base64, mp3_paths))
        return results

async def speech_to_text(postgres,mp3_paths):
    domain = "192.168.1.161"
    transcribe = Transcribe()
    base64_converter = Base64()
    base64_audios = base64_converter.get_base64_conversions(mp3_paths)
    await transcribe.transcribe_multiple_audios(domain, base64_audios, postgres, mp3_paths)


