from pydantic import BaseModel

import pkvid.blender as blender


class ProjectConfig(BaseModel):
    name: str

class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
    def render(self):
        blender.render_video()
