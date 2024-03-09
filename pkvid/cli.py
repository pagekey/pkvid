import argparse
import sys

# from pkvid.config import get_config
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
    elif args.command == 'render':
        print("render", args.filename)
        # project_config = get_config(args.filename)
        # project = Project(project_config)
        # print(f"Successfully parsed project: {project.config.name}")
        # dirname = os.path.dirname(args.filename)
        # if len(dirname) > 0:
        #     # if not already in that dir, go to it
        #     os.chdir(os.path.dirname(args.filename))
        # os.makedirs('render', exist_ok=True)
        # os.chdir('render')
        # project.render()
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
