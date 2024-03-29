import argparse


runserver_parser = argparse.ArgumentParser(description='Runserver options', add_help=True)
runserver_parser.add_argument('-H', type=str, help='Specify the host to run the server')
runserver_parser.add_argument('-p', type=int, help='Specify the port to run the server')
runserver_parser.add_argument('-w', type=int, help='Specify the number of workers to use')

create_app_parser = argparse.ArgumentParser(description='Create application', add_help=True)
create_app_parser.add_argument('title', type=str, help='Specify the title of creating application')
create_app_parser.add_argument('-d', type=str, help='Specify the directory of the creating application')

test_parser = argparse.ArgumentParser(description='Run tests', add_help=True)
test_parser.add_argument('-H', type=str, help='Specify the host to run the test server')
test_parser.add_argument('-p', type=int, help='Specify the port to run the test server')

main_parser = argparse.ArgumentParser(description='Manage.py deployment tool')
main_parser.add_argument('file', type=str, help='Executive file')
main_parser.add_argument('command', choices=[
                                'runserver',
                                'createapp',
                                'test',
                                'crowl'
                            ],
                         type=str, help='Command to execute')
