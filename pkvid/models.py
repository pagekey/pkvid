from __future__ import annotations
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class ClipType(Enum):
    FILTER = 'filter'
    SUBPROJECT = 'subproject'
    TEXT = 'text'
    VIDEO = 'video'

class CartesianPair(BaseModel):
    x: float
    y: float

class Clip(BaseModel):
    type: ClipType
    channel: Optional[int] = 1
    start_with_last: Optional[bool] = False
    start_frame: Optional[int] = -1
    offset: Optional[CartesianPair] = CartesianPair(x=0, y=0)
    scale: Optional[CartesianPair] = CartesianPair(x=1, y=1)

class SubProject(Clip):
    type: ClipType = ClipType.SUBPROJECT
    project: ProjectConfig

class Text(Clip):
    type: ClipType = ClipType.TEXT
    body: str
    length: Optional[int] = 30
    size: Optional[float] = 96

class Filter(Clip):
    type: ClipType = ClipType.FILTER
    module: str
    function: str
    video: Video

class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[Filter, SubProject, Text, Video]]
