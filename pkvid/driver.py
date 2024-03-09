import os
import shutil
import tempfile



class BlenderDriverError(Exception):
    """Base class for BlenderDriver errors"""
    pass


class BlenderDriver:

    def __init__(self, debug=False):
        self._debug = debug
        self._commands = ['import bpy']

    def execute(self):
        if shutil.which('blender'):
            with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
                if self._debug:
                    debug_file = open('blender_driver_debug.py', 'w')
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
    
    def render_video(self, filename='output.mp4', frame_start=1, frame_end=10, use_vse=False):
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

    def add_video(self, filename, channel=1, start_frame=1):
        self._commands.append('scene = bpy.context.scene')
        self._commands.append('sequence_editor = scene.sequence_editor')

        # Create a new sequence if one doesn't exist
        self._commands.append('if sequence_editor is None:')
        self._commands.append('    sequence_editor = scene.sequence_editor_create()')

        # Add the video file to the sequence editor as a video strip
        self._commands.append('video_strip = sequence_editor.sequences.new_movie(')
        self._commands.append('    frame_start=%d,' % start_frame)
        self._commands.append('    name="%s",' % filename)
        self._commands.append('    filepath="%s",' % os.path.join('..', filename))  # since we are in the render dir
        self._commands.append('    channel=%d' % channel)
        self._commands.append(')')
