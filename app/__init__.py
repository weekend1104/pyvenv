from flask import Flask

app = Flask(__name__, template_folder='temphtml', static_folder='static')

from app import views