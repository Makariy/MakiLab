All tests are run by manage.py with argument < test >.

To create a test, you need to subclass from <lib.test.TestCase>. 
All the asynchronous functions starting with 'test_' of this subclass
will be tested. To set up testing data you can override asynchronous function
setUp. 