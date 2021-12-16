import os
import sys
from lib.arg_parser import main_parser, \
    runserver_parser, \
    create_app_parser, \
    test_parser
from lib.tester import Tester

from src.application import run_app
import config


def main(args):
    """This function is starting and configuring the hole sanic application"""
    args, extra = args

    if args.command == 'runserver':
        if 'help' in extra:
            runserver_parser.print_help()
            return

        args = runserver_parser.parse_args(extra)
        run_app(
            host=args.H or 'localhost',
            port=args.p or 8000,
            workers=args.w or 1,
            config=config
        )

    elif args.command == 'test':
        if 'help' in extra:
            test_parser.print_help()
            return

        args = test_parser.parse_args(extra)

        tester = Tester()
        tester.run(run_app, config, args)

    elif args.command == 'createapp':
        if 'help' in extra:
            create_app_parser.print_help()
            return
        args = create_app_parser.parse_args(extra)
        raise NotImplemented()


if __name__ == '__main__':
    os.environ.setdefault('SANIC_APP_NAME', os.environ.get('SANIC_APP_NAME') or 'sanic_application')
    arguments = main_parser.parse_known_args(sys.argv)
    main(arguments)
