from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/led/rainbow')
def led_rainbow():
    app.hexapod.led.rainbow()
    return "Rainbow"
