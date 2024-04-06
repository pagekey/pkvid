from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import importlib
import json
import os
from typing import Optional, Union

from pydantic import BaseModel
import yaml

from pkvid.driver import BlenderDriver
from moviepy.video.io.VideoFileClip import VideoFileClip

from pkvid.models import CartesianPair

def video_length(filename: str):
    clip = VideoFileClip(filename)
    seconds = clip.duration
    fps = 30
    duration = int(seconds * fps)
    clip.close()
    return duration

class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[Filter, SubProject, Text, Video]]

    def save(self, filename: str):
        with open(filename, 'w') as file:
            # slight workaround: json first, then yaml
            # otherwise, dumping ClipType gets messed up
            json_str = self.model_dump_json()
            # convert to yaml
            config_dict = json.loads(json_str)
            yaml.dump(config_dict, file)
    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            config_dict = yaml.safe_load(file)
            config = ProjectConfig(**config_dict)
        return config
    
    def get_output_filename(self):
        return f"{self.name}.mp4"

    def render(self, driver: BlenderDriver = None):
        if driver is None:
            driver = BlenderDriver(name=self.name, debug=True)
        # Use driver to render project
        total_length = 0
        clip_lengths = []
        for idx, clip in enumerate(self.clips):
            if clip.start_with_last:
                if idx < 1:
                    raise ValueError("start_with_last set for first clip")
                ref_idx = idx - 1
                while self.clips[ref_idx].start_with_last:
                    ref_idx -= 1
                start_frame = total_length - clip_lengths[ref_idx]
            else:
                start_frame = total_length
            clip_length = clip.render(driver, start_frame=start_frame)
            clip_lengths.append(clip_length)
            if clip.start_with_last:
                # If we start w/ last, only increase length by the amount
                # that this clip is LONGER than the last one
                amount_increased = clip_length - clip_lengths[ref_idx]
                if amount_increased > 0:
                    total_length += amount_increased
            else:
                total_length += clip_length
        driver.save_project(f'{self.name}.blend')
        driver.render_video(self.get_output_filename(), frame_end=total_length)
        driver.execute()


class ClipType(str, Enum):
    FILTER = 'filter'
    SUBPROJECT = 'subproject'
    TEXT = 'text'
    VIDEO = 'video'


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
        # Render the subproject to a video file
        self.project.render()
        # Add that rendered video to project
        abspath = os.path.abspath(self.project.get_output_filename())
        return Video(path=abspath, channel=self.channel).render(driver, start_frame=start_frame)


class Text(Clip):
    type: ClipType = ClipType.TEXT
    body: str
    length: Optional[int] = 30
    size: Optional[float] = 96

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        driver.add_text(
            self.body,
            self.offset,
            self.scale,
            start_frame=start_frame, 
            end_frame=start_frame + self.length,
            channel=self.channel,
        )
        return self.length


class Filter(Clip):
    type: ClipType = ClipType.FILTER
    module: str
    function: str
    video: Video

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        # Run filter to get the ProjectConfig
        lib = importlib.import_module(self.module)
        func = getattr(lib, self.function)
        self.video.path = os.path.abspath(os.path.join('..', self.video.path))
        output = func(self.video)
        # Add ProjectConfig as a SubProject
        subp = SubProject(
            offset=self.offset,
            start_with_last=self.start_with_last,
            scale=self.scale,
            project=output,
            start_frame=start_frame,
        )
        return subp.render(driver, start_frame=start_frame)


class Video(Clip):
    type: ClipType = ClipType.VIDEO
    path: str

    def render(self, driver: BlenderDriver, start_frame: int = 0) -> int:
        # join with .. because we are currently cwd'd into the build folder
        abspath = os.path.abspath(os.path.join('..', self.path))
        driver.add_video(
            abspath, 
            offset=self.offset, 
            scale=self.scale, 
            start_frame=start_frame, 
            channel=self.channel
        )
        driver.add_audio(
            abspath, 
            start_frame=start_frame, 
            channel=self.channel + 1
        )
        return video_length(abspath)
