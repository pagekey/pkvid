import pkvid.blender as blender
from pkvid.models import ClipType, ProjectConfig


class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_filename = f"{self.config.name}.mp4"
        self.project_filename = f"{self.config.name}.blend"
    def render(self):
        blender.new_project()
        max_frame = 1
        for clip in self.config.clips:
            if clip.type == ClipType.SUBPROJECT:
                blender.save_project(self.project_filename)
                # Create and render the project
                project = Project(clip.project)
                project.render()
                # Reopen this project (the child had their own)
                blender.open_project(self.project_filename)
                # Add the renderer clip to this
                video = blender.add_video(project.output_filename, start_frame=max_frame)
                blender.add_audio(project.output_filename, start_frame=max_frame)
                max_frame += video.frame_final_duration
            elif clip.type == ClipType.TEXT:
                blender.add_text(clip.body, start_frame=max_frame, end_frame=max_frame + clip.length)
                max_frame += clip.length
            elif clip.type == ClipType.VIDEO:
                # Add the video based on clip.path
                video = blender.add_video(clip.path, start_frame=max_frame)
                # apply offset
                if clip.offset is not None:
                    video.transform.offset_x = int(clip.offset.x)
                    video.transform.offset_y = int(clip.offset.y)
                # apply scale
                if clip.scale is not None:
                    video.transform.scale_x = clip.scale.x
                    video.transform.scale_y = clip.scale.y
                blender.add_audio(clip.path, start_frame=max_frame)
                max_frame += video.frame_final_duration
        blender.save_project(self.project_filename)
        blender.render_video(filename=self.output_filename, frame_end=max_frame)
