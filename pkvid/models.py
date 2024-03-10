from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import os
import shutil
from typing import Optional, Union

from pydantic import BaseModel
import yaml

from pkvid.driver import BlenderDriver
from moviepy.video.io.VideoFileClip import VideoFileClip


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
    
    def render(self, driver: BlenderDriver = BlenderDriver(debug=True)):
        # Set up build directory
        shutil.rmtree('build', ignore_errors=True)
        orig_dir = os.getcwd()
        os.makedirs('build', exist_ok=True)
        os.chdir('build')
        # Use driver to render project
        total_length = 0
        for clip in self.clips:
            clip_length = clip.render(driver, start_frame=total_length)
            total_length += clip_length
        driver.save_project(f'{self.name}.blend')
        driver.render_video(f'{self.name}.mp4', frame_end=total_length)
        driver.execute()
        # Restore original directory
        os.chdir(orig_dir)


class ClipType(Enum):
    FILTER = 'filter'
    SUBPROJECT = 'subproject'
    TEXT = 'text'
    VIDEO = 'video'

class CartesianPair(BaseModel):
    x: float
    y: float


class Clip(BaseModel, ABC):
    type: ClipType
    channel: Optional[int] = 1
    start_with_last: Optional[bool] = False
    start_frame: Optional[int] = -1
    offset: Optional[CartesianPair] = CartesianPair(x=0, y=0)
    scale: Optional[CartesianPair] = CartesianPair(x=1, y=1)

    @abstractmethod
    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        """
        Use the driver to render this clip.

        Returns:
            The length of the clip rendered.
        """
        pass


class SubProject(Clip):
    type: ClipType = ClipType.SUBPROJECT
    project: ProjectConfig

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        return 0


class Text(Clip):
    type: ClipType = ClipType.TEXT
    body: str
    length: Optional[int] = 30
    size: Optional[float] = 96

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        driver.add_text(self.body, start_frame=start_frame, end_frame=start_frame + self.length)
        return self.length


class Filter(Clip):
    type: ClipType = ClipType.FILTER
    module: str
    function: str
    video: Video

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        return 0


class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        # join with .. because we are currently cwd'd into the build folder
        abspath = os.path.abspath(os.path.join('..', self.path))
        driver.add_video(abspath, start_frame=start_frame)
        driver.add_audio(abspath, start_frame=start_frame)
        # Determine length of clip
        clip = VideoFileClip(abspath)
        seconds = clip.duration
        fps = 30
        duration = int(seconds * fps)
        clip.close()
        return duration
