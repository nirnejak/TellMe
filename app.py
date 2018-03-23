# Librarys
from flask import Flask

# Variables
app = Flask(__name__)

# Settings
app.config.from_pyfile('config.py')

from views import *
from api import *

# Run
if __name__ == '__main__':
    app.run()