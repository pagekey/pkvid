import bpy
import os


def new_project():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def open_project(filename):
    abs_filename = os.path.abspath(filename)
    bpy.ops.wm.open_mainfile(filepath=abs_filename)

def save_project(filename):
    abs_filename = os.path.abspath(filename)
    if os.path.exists(abs_filename):
        os.remove(abs_filename)
    bpy.ops.wm.save_as_mainfile(filepath=abs_filename)

def render_video(filename='output.mp4', frame_start=1, frame_end=10, use_vse=False):
    scene = bpy.context.scene
    scene.render.filepath = filename
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


def add_video(filename, channel=1, start_frame=1):
    scene = bpy.context.scene
    sequence_editor = scene.sequence_editor

    # Create a new sequence if one doesn't exist
    if sequence_editor is None:
        sequence_editor = scene.sequence_editor_create()

    # Add the video file to the sequence editor as a video strip
    video_strip = sequence_editor.sequences.new_movie(
        frame_start=start_frame,
        name="VideoStrip",
        filepath=filename,
        channel=channel
    )

    return video_strip

def add_audio(filename, channel=1, start_frame=1):
    scene = bpy.context.scene
    sequence_editor = scene.sequence_editor

    # Create a new sequence if one doesn't exist
    if sequence_editor is None:
        sequence_editor = scene.sequence_editor_create()

    # Add the audio file to the sequence editor as an audio strip
    audio_strip = sequence_editor.sequences.new_sound(
        frame_start=start_frame,
        name="AudioStrip",
        filepath=filename,
        channel=channel
    )
    return audio_strip

def add_text(body: str, frame_start=1, frame_end=31):
    text_strip = bpy.context.scene.sequence_editor.sequences.new_effect(
        name="MyText", type="TEXT", channel=1, frame_start=frame_start,
        frame_end=frame_end,
    )
    text_strip.text = body
    text_strip.font_size = 96
    text_strip.color = (0.0, 0.0, 0.0, 1.0)
    text_strip.location.x = 0.5
    text_strip.location.y = 0.5
    return text_strip
