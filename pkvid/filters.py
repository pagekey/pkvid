from pkvid.models import ProjectConfig, Video


def add_captions(video: Video) -> ProjectConfig:
    return ProjectConfig(
        name=f"{video.path}-add_captions",
        clips=[video],
    )
