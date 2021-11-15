from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/mpu')
def mpu():
    return {'pitch': app.hexapod.mpu.current_pitch,
            'roll': app.hexapod.mpu.current_roll,
            'yaw': app.hexapod.mpu.current_yaw
            }
