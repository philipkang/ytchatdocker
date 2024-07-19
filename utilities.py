import logging
from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger()
logger.setLevel("INFO")

def get_video_id_from_url(youtube_url):
    logger.info("Inside get_video_id_from_url ..")

    watch_param = 'watch?v='
    video_id = youtube_url.split('/')[-1].strip()
    if video_id == '':
        video_id = youtube_url.split('/')[-2].strip()
    if watch_param in video_id:
        video_id = video_id[len(watch_param):]

    logger.info("video_id")
    logger.info(video_id)
    return video_id

def get_transcript(video_id):
    logger.info("Inside get_transcript ..")

    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    logger.info("transcript")
    logger.info(transcript)
    return transcript

def generate_prompt_from_transcript(transcript):
    logger.info("Inside generate_prompt_from_transcript ..")

    prompt = "Summarize the following video:\n"
    for trans in transcript:
        prompt += " " + trans.get('text', '')
    
    logger.info("prompt")
    logger.info(prompt)
    return prompt