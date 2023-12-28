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
        for clip in self.config.clips:
            blender.add_video(clip.path)
            blender.add_audio(clip.path)
        blender.render_video()
