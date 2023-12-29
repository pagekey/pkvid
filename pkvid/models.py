from __future__ import annotations
from enum import Enum
from typing import Union

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

class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[SubProject, Text, Video]]
