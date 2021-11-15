from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/ultrasonic')
def ultrasonic():
    return {'ultrasonic': app.hexapod.ultrasonic.current_distance}
