import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from core.main.routes import main
from core.product.routes import product
app.register_blueprint(main)
app.register_blueprint(product)