Application pattern:
- tests/* - contains the tests to run in the application
- routes.py - contains the blueprint and initializes the routes on it
- models.py - contains the models that it uses
- app.py - must contain a blueprint < bp > that will be used in application routes and general blueprint_patterns 

  [Optionally]
- services/ - a directory that contains the services that the application uses 