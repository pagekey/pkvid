from enum import Enum

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
    # project: ProjectConfig