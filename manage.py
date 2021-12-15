import os, sys
from arg_parser import main_parser, runserver_parser, create_app_parser
from src.server import run_app
import config


def main(args):
    """This function is starting and configuring the hole sanic application"""
    args, extra = args

    if args.command == 'runserver':
        args = runserver_parser.parse_args(extra)
        run_app(
            host=args.H or 'localhost',
            port=args.p or 8000,
            workers=args.w or 1,
            config=config
        )

    if args.command == 'createapp':
        args = create_app_parser.parse_args(extra)
        raise NotImplemented()


if __name__ == '__main__':
    os.environ.setdefault('SANIC_APP_NAME', os.environ.get('SANIC_APP_NAME') or 'sanic_application')
    arguments = main_parser.parse_known_args(sys.argv)
    main(arguments)
