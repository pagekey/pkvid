import pkvid.blender as blender
from pkvid.models import ClipType, ProjectConfig


class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_filename = f"{self.config.name}.mp4"
    def render(self):
        max_frame = 1
        for clip in self.config.clips:
            if clip.type == ClipType.SUBPROJECT:
                # Create and render the project
                project = Project(clip.project)
                project.render()
                # Add the renderer clip to this
                video = blender.add_video(project.output_filename, start_frame=max_frame)
                blender.add_audio(project.output_filename, start_frame=max_frame)
                max_frame += video.frame_final_duration
            elif clip.type == ClipType.VIDEO:
                # Add the video based on clip.path
                video = blender.add_video(clip.path, start_frame=max_frame)
                blender.add_audio(clip.path, start_frame=max_frame)
                max_frame += video.frame_final_duration
        blender.render_video(filename=self.output_filename, frame_end=max_frame)
