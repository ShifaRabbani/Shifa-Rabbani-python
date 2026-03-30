import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlalchemy as db
from flask import Blueprint , jsonify , request

from database.connection import get_engine
