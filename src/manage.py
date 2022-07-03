import os
import sys
from src.lib.arg_parser import main_parser, \
    runserver_parser, \
    create_app_parser, \
    test_parser
from src.lib.tester import Tester
from src.lib.start_new_app import start_new_app

from src.application import create_app, run_app
import config 

from src.crowler.crowl import crowl


def main(args):
    """This function is starting and configuring the hole sanic application"""
    args, extra = args

    if args.command == 'runserver':
        if 'help' in extra:
            runserver_parser.print_help()
            return

        args = runserver_parser.parse_args(extra)
        app = create_app(config=config)
        run_app(
            app=app,
            host=args.H or 'localhost',
            port=args.p or 8000,
            workers=args.w or 1,
        )

    elif args.command == 'test':
        if 'help' in extra:
            test_parser.print_help()
            return

        args = test_parser.parse_args(extra)

        app = create_app(config)
        tester = Tester()
        tester.run(app, config, args)

    elif args.command == 'createapp':
        if 'help' in extra:
            create_app_parser.print_help()
            return
        args = create_app_parser.parse_args(extra)
        start_new_app(args.title)

    elif args.command == 'crowl':
        app = create_app(config)
        crowl(app)


if __name__ == '__main__':
    os.environ.setdefault('SANIC_APP_NAME', os.environ.get('SANIC_APP_NAME') or 'sanic_application')
    arguments = main_parser.parse_known_args(sys.argv)
    main(arguments)
