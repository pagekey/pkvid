import pkvid.blender as blender
from pkvid.models import ClipType, ProjectConfig, SubProject, Text, Video


class Project:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.output_filename = f"{self.config.name}.mp4"
        self.project_filename = f"{self.config.name}.blend"
    def add_subproject(self, clip: SubProject):
        blender.save_project(self.project_filename)
        # Create and render the project
        project = Project(clip.project)
        project.render()
        # Reopen this project (the child had their own)
        blender.open_project(self.project_filename)
        # Add the pre-rendered video
        video_clip = Video(path=project.output_filename, start_frame=clip._start_frame, channel=clip.channel)
        video_clip._start_frame = clip._start_frame
        video = self.add_video(video_clip)
        clip._end_frame = video_clip._end_frame
        return video
    def add_text(self, clip: Text):
        clip._end_frame = clip._start_frame + clip.length
        text = blender.add_text(clip.body, start_frame=clip._start_frame, end_frame=clip._end_frame, channel=clip.channel)
        return text
    def add_video(self, clip: Video):
        # Add the video based on clip.path
        video = blender.add_video(clip.path, start_frame=clip._start_frame, channel=clip.channel)
        blender.add_audio(clip.path, start_frame=clip._start_frame, channel=clip.channel + 1)
        clip._end_frame = clip._start_frame + video.frame_final_duration
        return video
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
            
            visual_object = None
            # Take special actions based on clip type
            if clip.type == ClipType.SUBPROJECT:
                visual_object = self.add_subproject(clip)
            elif clip.type == ClipType.TEXT:
                visual_object = self.add_text(clip)
            elif clip.type == ClipType.VIDEO:
                visual_object = self.add_video(clip)

            # apply offset
            visual_object.transform.offset_x = int(clip.offset.x)
            visual_object.transform.offset_y = int(clip.offset.y)
            # apply scale
            visual_object.transform.scale_x = clip.scale.x
            visual_object.transform.scale_y = clip.scale.y
            # Set clip._end_frame
            max_frame = max(max_frame, clip._end_frame)
            if last_clip:
                max_frame = max(max_frame, clip._end_frame, last_clip._end_frame)
        blender.save_project(self.project_filename)
        blender.render_video(filename=self.output_filename, frame_end=max_frame)
