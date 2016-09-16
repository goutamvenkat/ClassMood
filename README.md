# ClassMood

# Installing Requirements
All application requirements are held in requirements.txt and can be installed with "pip install -r requirements.txt"

# Application Layout
The application is generally divided into the following structure:
- runserver.py: Runs the application and starts the dev server
- Class Mood App: The main directory for the application
    - Config: Contains the necessary config files for the application
    - Controllers: All of the controllers for the application, which include the routes needed for each action
    - Models: The different models for the application
        - DBModels: All of the application models that map to the database
    - db: Contains the various SQLite databases used by the app
    - static: All static content for the app
        - css: Stylesheets for the app
        - fonts: Fonts used by the app
        - img: Images used by the app
        - js: Javascript app files for Angular
        - lib: Javascript libraries used by the app
        - partials: Partial view templates used by Angular
    - templates: templates used by Flask for rendering