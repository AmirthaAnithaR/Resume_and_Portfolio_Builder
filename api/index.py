import sys
import os

# Add the resume-portfolio-builder directory to the path
# so that app.py can import database.py as a sibling module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'resume-portfolio-builder'))

from app import app
