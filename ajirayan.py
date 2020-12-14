from flask import Flask
from rover import rover_blueprint
from planet import planet_blueprint

app = Flask(__name__)
app.register_blueprint(planet_blueprint, url_prefix="/api/environment")
app.register_blueprint(rover_blueprint, url_prefix="/api/rover")



