import argparse
from pkvid.blender import render_video

from pkvid.config import get_config
from pkvid.project import Project


def main():
    parser = argparse.ArgumentParser(description='Video editing toolkit')
    parser.add_argument('filename', help='Name of config file')
    args = parser.parse_args()

    if args.filename:
        project_config = get_config(args.filename)
        project = Project(project_config)
        print(f"Successfully parsed project: {project.config.name}")
        render_video()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
