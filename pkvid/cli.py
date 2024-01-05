import argparse
import os
import sys

import pkvid.blender as blender
from pkvid.config import get_config
from pkvid.project import Project


def main(cli_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Video editing toolkit')
    parser.add_argument('filename', help='Name of config file')
    args = parser.parse_args(cli_args)

    if args.filename:
        project_config = get_config(args.filename)
        project = Project(project_config)
        print(f"Successfully parsed project: {project.config.name}")
        os.chdir(os.path.dirname(args.filename))
        os.makedirs('render', exist_ok=True)
        os.chdir('render')
        project.render()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
