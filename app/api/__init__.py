from flask import Blueprint
# 等同于demo_main.py中的 app = Flask()
api = Blueprint('api', __name__)

from . import cypress
from . import test
