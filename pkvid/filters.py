import os

import whisper

import pkvid.blender as blender
from pkvid.models import CartesianPair, ProjectConfig, Text, Video


def add_captions(video: Video) -> ProjectConfig:
    # Generate transcription
    print("Generating transcription...")
    model = whisper.load_model('base')
    result = model.transcribe(video.path)
    # Convert Whisper segments to Text
    texts = []
    for segment in result['segments']:
        start_sec = segment['start']
        end_sec = segment['end']
        FPS = 30 # TODO likely should not be hard coded
        start_frame = int(start_sec * FPS)
        end_frame = int(end_sec * FPS)
        text = Text(
            channel=3,
            body=segment['text'],
            start_frame=start_frame,
            length=end_frame - start_frame,
            start_with_last=True,
            offset=CartesianPair(x=0, y=-338),
            size=60,
        )
        texts.append(text)
    # Generate ProjectConfig
    return ProjectConfig(
        name=f"{os.path.basename(video.path)}-add_captions",
        clips=[
            video,
            *texts,
        ],
    )
