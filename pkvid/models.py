from __future__ import annotations
from enum import Enum
import json
from typing import Optional, Union

from pydantic import BaseModel
import yaml

from pkvid.driver import BlenderDriver


class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[Filter, SubProject, Text, Video]]

    def save(self, filename: str):
        with open(filename, 'w') as file:
            yaml.dump(self.model_dump(), file)
        print("Wrote", filename)
    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            config_dict = yaml.safe_load(file)
            config = ProjectConfig(**config_dict)
        return config
    
    def render(self, driver: BlenderDriver = BlenderDriver()):
        driver.save_project(f'{self.name}.blend')
        driver.render_video()
        driver.execute()


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
