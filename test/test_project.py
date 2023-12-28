from unittest.mock import patch
import pytest

from pkvid.project import Project, ProjectConfig


@pytest.fixture
def project():
    config = ProjectConfig(name='hi')
    return Project(config)


@patch("pkvid.blender.render_video")
def test_render(mock_render_video, project):
    project.render()
    mock_render_video.assert_called()
