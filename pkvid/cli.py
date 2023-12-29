import argparse
import sys

import pkvid.blender as blender
from pkvid.config import get_config
from pkvid.project import Project


def main(cli_args=sys.argv[1:]):
    while cli_args[0] == '-b' or cli_args[0] == '-P' or 'pkvid' in cli_args[0]:
        # chop off blender -b -P blah blah blah
        cli_args = cli_args[1:]
    parser = argparse.ArgumentParser(description='Video editing toolkit')
    parser.add_argument('filename', help='Name of config file')
    args = parser.parse_args(cli_args)

    if args.filename:
        project_config = get_config(args.filename)
        project = Project(project_config)
        print(f"Successfully parsed project: {project.config.name}")
        project.render()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
