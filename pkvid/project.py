import pkvid.blender as blender
from pkvid.models import ClipType, ProjectConfig


class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
    def render(self):
        max_frame = 1
        for clip in self.config.clips:
            if clip.type == ClipType.SUBPROJECT:
                pass
            elif clip.type == ClipType.VIDEO:
                video = blender.add_video(clip.path, start_frame=max_frame)
                blender.add_audio(clip.path, start_frame=max_frame)
                max_frame += video.frame_final_duration
        blender.render_video(filename=f"{self.config.name}.mp4", frame_end=max_frame)
