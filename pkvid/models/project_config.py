from typing import Union
from pydantic import BaseModel

from pkvid.models.clip import SubProject, Video


class ProjectConfig(BaseModel):
    name: str
    clips: list[Union[Video, SubProject]]
