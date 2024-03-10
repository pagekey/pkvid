import argparse
import os
import shutil
import sys

from pkvid.models import ProjectConfig
# from pkvid.project import Project


def main(cli_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Video editing toolkit')
    subparsers = parser.add_subparsers(dest='command')

    new_parser = subparsers.add_parser('new', help='Create a new project')

    render_parser = subparsers.add_parser('render', help='Render a project')
    render_parser.add_argument('-f', '--filename', help='Name of config file', default='pkvid.yaml')

    args = parser.parse_args(cli_args)

    if args.command == 'new':
        print("Create a new project here")
        # Read a string for the name from the user
        name = input("What is the name of the project? ")
        config = ProjectConfig(name=name, clips=[])
        config.save('pkvid.yaml')
    elif args.command == 'render':
        print("render", args.filename)
        config = ProjectConfig.load(args.filename)
        print(f"Successfully parsed project: {config.name}")
        # Set up build directory
        shutil.rmtree('build', ignore_errors=True)
        orig_dir = os.getcwd()
        os.makedirs('build', exist_ok=True)
        os.chdir('build')
        # Perform render of project
        config.render()
        # Restore original directory
        os.chdir(orig_dir)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
