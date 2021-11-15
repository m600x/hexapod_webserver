from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/servo/enable')
def servo_enable():
    app.hexapod.servo.enable_servo()
    return {'servo': app.hexapod.servo.servo_enabled}


@routes.route('/api/servo/disable')
def servo_disable():
    app.hexapod.servo.disable_servo()
    return {'servo': app.hexapod.servo.servo_enabled}
