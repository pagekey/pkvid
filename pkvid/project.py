from pydantic import BaseModel


class ProjectConfig(BaseModel):
    name: str

class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
