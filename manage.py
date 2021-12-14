import argparse
import sys
from src.server import run_app
import config


parser = argparse.ArgumentParser(description='Manage.py deployment tool')
parser.add_argument('file', type=str, help='Command to execute')
parser.add_argument('command', type=str, help='Command to execute')
parser.add_argument('-H', type=str, help='Specify the host to run the server')
parser.add_argument('-p', type=int, help='Specify the port to run the server')
parser.add_argument('-w', type=int, help='Specify the number of workers to use')


def main(args):
    """This function is starting and configuring the hole sanic application"""
    if args.command == 'runserver':
        run_app(
            host=args.H or 'localhost',
            port=args.p or 8000,
            workers=args.w or 1,
            config=config
        )


if __name__ == '__main__':
    arguments = parser.parse_args(sys.argv)
    main(arguments)
