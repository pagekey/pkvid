from unittest.mock import patch
import pytest

from pkvid.project import Clip, Project, ProjectConfig


@pytest.fixture
def project():
    config = ProjectConfig(name='hi', clips=[])
    return Project(config)


@patch("pkvid.blender.render_video")
def test_render(mock_render_video, project):
    project.render()
    mock_render_video.assert_called()

@patch("pkvid.blender.add_audio")
@patch("pkvid.blender.add_video")
@patch("pkvid.blender.render_video")
def test_render_clips(mock_render_video, mock_add_video, mock_add_audio, project):
    project.config.clips = [Clip(type='video', path='some_path')]
    project.render()
    mock_add_video.assert_called_with('some_path')
    mock_add_audio.assert_called_with('some_path')
    mock_render_video.assert_called()
