import os
import shutil
import tempfile

from pkvid.models2 import CartesianPair



class BlenderDriverError(Exception):
    """Base class for BlenderDriver errors"""
    pass


class BlenderDriver:

    def __init__(self, name="default", debug=False):
        self.name = name
        self._debug = debug
        self._commands = ['import bpy']

    def execute(self):
        if shutil.which('blender'):
            with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
                if self._debug:
                    debug_file = open('blender_driver_debug_%s.py' % self.name, 'w')
                for line in self._commands:
                    text_to_file = line + '\n'
                    temp_file.write(text_to_file)
                    if self._debug:
                        debug_file.write(text_to_file)
                if self._debug:
                    debug_file.close()
                temp_file.flush()
                os.system('blender -b -P %s' % temp_file.name)
        else:
            raise BlenderDriverError('Blender not found on PATH')

    def new_project(self, filename):
        abs_filename = os.path.abspath(filename)
        self._commands.append('bpy.ops.wm.open_mainfile(filepath="%s"' % abs_filename)

    def open_project(self, filename):
        abs_filename = os.path.abspath(filename)
        self._commands.append('bpy.ops.wm.open_mainfile(filepath="%s"' % abs_filename)

    def save_project(self, filename):
        self._commands.append('bpy.context.scene.render.fps = 30')
        abs_filename = os.path.abspath(filename)
        if os.path.exists(abs_filename):
            os.remove(abs_filename)
        self._commands.append('bpy.ops.wm.save_as_mainfile(filepath="%s")' % abs_filename)
    
    def render_video(self, filename='output.mp4', frame_start=1, frame_end=10, use_vse=True):
        self._commands.append('scene = bpy.context.scene')
        self._commands.append('scene.render.filepath = "%s"' % filename)
        self._commands.append('scene.render.resolution_x = 1920')
        self._commands.append('scene.render.resolution_y = 1080')
        self._commands.append('scene.frame_start = %d' % frame_start)
        self._commands.append('scene.frame_end = %d' % frame_end)
        self._commands.append('scene.render.image_settings.file_format = "FFMPEG"')
        self._commands.append('scene.render.ffmpeg.format = "MPEG4"')
        self._commands.append('scene.render.ffmpeg.audio_codec = "MP3"')
        if use_vse:
            # Set rendering to use the VSE sequence
            self._commands.append('scene.sequence_editor_create()')  # Ensure sequence editor exists
            self._commands.append('scene.render.use_sequencer = True')

        self._commands.append('bpy.ops.render.render(animation=True)')

    def add_video(self, filename, offset: CartesianPair, scale: CartesianPair, channel=1, start_frame=1):
        self._commands.append('scene = bpy.context.scene')
        self._commands.append('sequence_editor = scene.sequence_editor')

        # Create a new sequence if one doesn't exist
        self._commands.append('if sequence_editor is None:')
        self._commands.append('    sequence_editor = scene.sequence_editor_create()')

        # Add the video file to the sequence editor as a video strip
        self._commands.append('video_strip = sequence_editor.sequences.new_movie(')
        self._commands.append('    frame_start=%d,' % start_frame)
        self._commands.append('    name="%s",' % filename)
        self._commands.append('    filepath="%s",' % filename)
        self._commands.append('    channel=%d' % channel)
        self._commands.append(')')
        self._commands.append('video_strip.transform.offset_x = %d' % offset.x)
        self._commands.append('video_strip.transform.offset_y = %d' % offset.y)
        self._commands.append('video_strip.transform.scale_x = %f' % scale.x)
        self._commands.append('video_strip.transform.scale_y = %f' % scale.y)

    def add_audio(self, filename, channel=2, start_frame=1):
        self._commands.append('scene = bpy.context.scene')
        self._commands.append('sequence_editor = scene.sequence_editor')

        # Create a new sequence if one doesn't exist
        self._commands.append('if sequence_editor is None:')
        self._commands.append('    sequence_editor = scene.sequence_editor_create()')

        # Add the audio file to the sequence editor as an audio strip
        self._commands.append('audio_strip = sequence_editor.sequences.new_sound(')
        self._commands.append('    frame_start=%d,' % start_frame)
        self._commands.append('    name="AudioStrip",')
        self._commands.append('    filepath="%s",' % filename)
        self._commands.append('    channel=%d' % channel)
        self._commands.append(')')

    def add_text(self, body: str, offset: CartesianPair, scale: CartesianPair, start_frame=1, end_frame=31, channel=1, size=96):
        self._commands.append('sequence_editor = bpy.context.scene.sequence_editor')
        self._commands.append('text_strip = sequence_editor.sequences.new_effect(')
        self._commands.append('    name="MyText",')
        self._commands.append('    type="TEXT",')
        self._commands.append('    channel=%d,' % channel)
        self._commands.append('    frame_start=%d,' % start_frame)
        self._commands.append('    frame_end=%d' % end_frame)
        self._commands.append(')')
        self._commands.append('text_strip.text = "%s"' % body)
        self._commands.append('text_strip.font_size = %d' % size)
        self._commands.append('text_strip.color = (1.0, 1.0, 1.0, 1.0)')
        self._commands.append('text_strip.transform.offset_x = %d' % offset.x)
        self._commands.append('text_strip.transform.offset_y = %d' % offset.y)
        self._commands.append('text_strip.transform.scale_x = %f' % scale.x)
        self._commands.append('text_strip.transform.scale_y = %f' % scale.y)

# def remove_video(video_strip):
#     sequencer = bpy.context.scene.sequence_editor
#     if sequencer is not None and video_strip.name in sequencer.sequences:
#         sequencer.sequences.remove(video_strip)

# def add_audio(filename, channel=2, start_frame=1):
#     scene = bpy.context.scene
#     sequence_editor = scene.sequence_editor

#     # Create a new sequence if one doesn't exist
#     if sequence_editor is None:
#         sequence_editor = scene.sequence_editor_create()

#     # Add the audio file to the sequence editor as an audio strip
#     audio_strip = sequence_editor.sequences.new_sound(
#         frame_start=start_frame,
#         name="AudioStrip",
#         filepath=os.path.join('..', filename), # since we are in the render dir
#         channel=channel
#     )
#     return audio_strip

