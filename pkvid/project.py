import pkvid.blender as blender
from pkvid.models import ClipType, ProjectConfig


class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_filename = f"{self.config.name}.mp4"
        self.project_filename = f"{self.config.name}.blend"
    def render(self):
        blender.new_project()
        max_frame = 0
        for idx, clip in enumerate(self.config.clips):
            last_clip = None
            # Set clip._start_frame
            if idx > 0:
                last_clip = self.config.clips[idx - 1]
            if clip.start_with_last and last_clip is not None:
                clip._start_frame = last_clip._start_frame
            else:
                clip._start_frame = max_frame
            
            # Take special actions based on clip type
            if clip.type == ClipType.SUBPROJECT:
                blender.save_project(self.project_filename)
                # Create and render the project
                project = Project(clip.project)
                project.render()
                # Reopen this project (the child had their own)
                blender.open_project(self.project_filename)
                # Add the renderer clip to this
                video = blender.add_video(project.output_filename, start_frame=clip._start_frame, channel=clip.channel)
                blender.add_audio(project.output_filename, start_frame=clip._start_frame, channel=clip.channel + 1)
                clip._end_frame = clip._start_frame + video.frame_final_duration
            elif clip.type == ClipType.TEXT:
                clip._end_frame = clip._start_frame + clip.length
                blender.add_text(clip.body, start_frame=clip._start_frame, end_frame=clip._end_frame, channel=clip.channel)
            elif clip.type == ClipType.VIDEO:
                # Add the video based on clip.path
                video = blender.add_video(clip.path, start_frame=clip._start_frame, channel=clip.channel)
                # apply offset
                video.transform.offset_x = int(clip.offset.x)
                video.transform.offset_y = int(clip.offset.y)
                # apply scale
                video.transform.scale_x = clip.scale.x
                video.transform.scale_y = clip.scale.y
                blender.add_audio(clip.path, start_frame=clip._start_frame, channel=clip.channel + 1)
                clip._end_frame = clip._start_frame + video.frame_final_duration
            
            # Set clip._end_frame
            clip._length = clip._end_frame - clip._start_frame
            if last_clip:
                max_frame = max(max_frame + clip._length, last_clip._end_frame)
            else:
                max_frame = max_frame + clip.length
        blender.save_project(self.project_filename)
        blender.render_video(filename=self.output_filename, frame_end=max_frame)
