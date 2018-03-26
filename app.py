# Librarys
from flask import Flask

# Variables
app = Flask(__name__)

# Settings
app.config.from_pyfile('config.py')

# Importing Views
from views import *
from api import *

from analysis import *

# Run
if __name__ == '__main__':
    app.run()