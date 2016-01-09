import sys
import os

project_path = os.path.sep.join(os.path.abspath(os.path.join(os.path.dirname(__file__))).split(os.path.sep)[:-1])
sys.path.append(project_path)

from app import app

if __name__ == '__main__':
    app.run()
