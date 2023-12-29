from __future__ import annotations
from enum import Enum
from typing import Optional, Tuple, Union

from pydantic import BaseModel


class ClipType(Enum):
    VIDEO = 'video'
    SUBPROJECT = 'subproject'
    TEXT = 'text'

class Clip(BaseModel):
    type: ClipType

class SubProject(Clip):
    type: ClipType = ClipType.SUBPROJECT
    project: ProjectConfig

class Text(Clip):
    type: ClipType = ClipType.TEXT
    body: str
    length: Optional[int] = 30

class VideoScale(BaseModel):
    x: float
    y: float

class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str
    scale: Optional[VideoScale] = VideoScale(x=1, y=1)

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[SubProject, Text, Video]]
