import sqlalchemy as db
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATABASE_URL

engine = db.create_engine(DATABASE_URL)

def get_engine():
    print("Creating database engine...")
    return engine