import pkvid.blender as blender
from pkvid.models import ProjectConfig, Text, Video


def add_captions(video: Video) -> ProjectConfig:
    # add video clip *only* to calculate its duration, then remove
    video_clip = blender.add_video(video.path)
    length = video_clip.frame_final_duration
    blender.remove_video(video_clip)
    # Generate ProjectConfig
    return ProjectConfig(
        name=f"{video.path}-add_captions",
        clips=[
            video,
            Text(
                channel=3,
                body="Here are the captions",
                length=length,
                start_with_last=True,
            ),
        ],
    )
