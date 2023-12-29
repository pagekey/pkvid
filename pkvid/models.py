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
    channel: Optional[int] = 1

class SubProject(Clip):
    type: ClipType = ClipType.SUBPROJECT
    project: ProjectConfig

class Text(Clip):
    type: ClipType = ClipType.TEXT
    body: str
    length: Optional[int] = 30

class CartesianPair(BaseModel):
    x: float
    y: float

class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str
    offset: Optional[CartesianPair] = CartesianPair(x=0, y=0)
    scale: Optional[CartesianPair] = CartesianPair(x=1, y=1)

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[SubProject, Text, Video]]
