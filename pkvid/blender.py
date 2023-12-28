import bpy


def render_video(frame_start=1, frame_end=10, use_vse=False):
    scene = bpy.context.scene
    scene.render.filepath = "output"
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_start = frame_start
    scene.frame_end = frame_end
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.audio_codec = 'MP3'

    if use_vse:
        # Set rendering to use the VSE sequence
        scene.sequence_editor_create()  # Ensure sequence editor exists
        scene.render.use_sequencer = True

    bpy.ops.render.render(animation=True)
