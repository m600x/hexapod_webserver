from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/adc/1')
def battery_voltage1():
    return {'voltage': app.hexapod.adc.current_b1_volt,
            'percentage': app.hexapod.adc.current_b1_pct}


@routes.route('/api/adc/2')
def battery_voltage2():
    return {'voltage': app.hexapod.adc.current_b2_volt,
            'percentage': app.hexapod.adc.current_b2_pct}
