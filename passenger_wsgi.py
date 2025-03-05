import sys
import os

# Add the application directory to the Python path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

# Import the Flask application
from app import app as application