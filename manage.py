import os
import sys
from lib.arg_parser import main_parser, runserver_parser, create_app_parser
from lib.run_test import Tester

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

    elif args.command == 'test':
        args = runserver_parser.parse_args(extra)
        config.DB_NAME = 'test_' + config.DB_NAME

        tester = Tester()

        from src.app_events import app_events
        app_events['before_server_start'].append(tester.run_all_tests)
        run_app('localhost', 8000, 1, config)

    elif args.command == 'createapp':
        args = create_app_parser.parse_args(extra)
        raise NotImplemented()


if __name__ == '__main__':
    os.environ.setdefault('SANIC_APP_NAME', os.environ.get('SANIC_APP_NAME') or 'sanic_application')
    arguments = main_parser.parse_known_args(sys.argv)
    main(arguments)
