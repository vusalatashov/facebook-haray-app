import os
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def download_and_convert_to_ogg(video_url, postgres):
    output_dir = 'resources/video_resources/'

    unique_id = video_url.split('=')[-1]

    try:
        # Download the video file
        ytdlp_command = [
            'yt-dlp',
            '-f', 'bestaudio',
            '--output', os.path.join(output_dir, f'{unique_id}.%(ext)s'),
            video_url
        ]
        process = await asyncio.create_subprocess_exec(
            *ytdlp_command,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()

        # Find the downloaded file
        input_file = None
        for file in os.listdir(output_dir):
            if file.startswith(unique_id) and file.endswith(('.mp4', '.mkv', '.webm', '.m4a', '.opus')):
                input_file = os.path.join(output_dir, file)
                break

        if input_file:
            output_file = os.path.join(output_dir, f'facebook-{unique_id}.ogg')

            # Convert the file to OGG format
            ffmpeg_command = [
                'ffmpeg',
                '-i', input_file,
                '-vn',
                '-acodec', 'libvorbis',
                output_file
            ]
            process = await asyncio.create_subprocess_exec(
                *ffmpeg_command,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.communicate()

            # Remove the original file to keep only the OGG file
            os.remove(input_file)

            # Update download status in the database
            postgres.update_download_status(video_url, output_file)

            logging.info(f"Video successfully converted to OGG format: facebook-{unique_id}.ogg")
            return True

        logging.error("Error: Downloaded file not found or could not be converted.")
        return False

    except Exception as e:
        logging.error(f"Error: {e}")
        return False


async def download_videos(postgres):
    tasks = []
    urls = postgres.get_post_url_for_download()
    for url in urls:
        task = asyncio.create_task(download_and_convert_to_ogg(url, postgres))
        tasks.append(task)

    await asyncio.gather(*tasks)
