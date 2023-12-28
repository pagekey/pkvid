import argparse

from pkvid.config import process_config


def main():
    parser = argparse.ArgumentParser(description='Video editing toolkit')
    parser.add_argument('filename', help='Name of config file')
    args = parser.parse_args()

    if args.filename:
        process_config(args.filename)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
