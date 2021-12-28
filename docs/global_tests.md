All tests are run by manage.py with argument < test >.
There is a fixture defined in file conftest.py that initializes an application every time every test is being executed.
This application is being passed as an argument to every test function to run. You can use application's asgi_client to 
make requests to the application. If you need to interact with database in your tests, use lib.tests.require_database 
decorator to attach database to the application. 
