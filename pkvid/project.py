from enum import Enum
from pydantic import BaseModel

import pkvid.blender as blender

class ClipType(Enum):
    VIDEO = 'video'

class Clip(BaseModel):
    type: ClipType
    path: str

class ProjectConfig(BaseModel):
    name: str
    clips: list[Clip]

class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
    def render(self):
        max_frame = 1
        for clip in self.config.clips:
            video = blender.add_video(clip.path, start_frame=max_frame)
            blender.add_audio(clip.path, start_frame=max_frame)
            max_frame += video.frame_final_duration
        blender.render_video(frame_end=max_frame)
