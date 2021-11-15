from flask import render_template
from flask import current_app as app
from . import routes


@routes.route('/api/buzzer')
def buzzer():
    app.hexapod.buzzer.toggle()
    return {'buzzer': app.hexapod.buzzer.status_buzzer}


@routes.route('/api/buzzer/<time_ms>')
def buzzer_ms(time_ms):
    app.hexapod.buzzer.active_ms(time_ms)
    return {'buzzer': app.hexapod.buzzer.status_buzzer}
