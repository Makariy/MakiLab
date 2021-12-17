Application pattern:
- tests.py - contains the tests to run in the application
- models.py - contains the models that it uses
- app.py - must contain the function <get_blueprint> that returns the blueprint that will be used in blueprint_patterns

    [Optionally]
- routes.py - contains the blueprint and initializes the routes on it 
- services/ - contains the services that the application uses 