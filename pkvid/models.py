from __future__ import annotations
from enum import Enum
from typing import Union

from pydantic import BaseModel


class ClipType(Enum):
    VIDEO = 'video'
    SUBPROJECT = 'subproject'

class Clip(BaseModel):
    type: ClipType

class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str

class SubProject(Clip):
    type: ClipType = ClipType.SUBPROJECT
    project: ProjectConfig

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[SubProject, Video]]
