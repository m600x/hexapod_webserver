#!/usr/bin/env python3
# coding:utf-8

import os
import time
import logging
import threading
from routes import *
from turbo_flask import Turbo
from flask import Flask, render_template
from Hexapod import Hexapod

LOG_FORMAT = "[%(asctime)s][ %(levelname)-8s ][ %(module)s:%(lineno)s ] %(message)s"
app = Flask(__name__)
app.register_blueprint(routes)
turbo = Turbo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_load():
    return app.hexapod.get_sensors()


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_data).start()


def update_data():
    with app.app_context():
        while True:
            time.sleep(0.5)
            turbo.push(turbo.replace(render_template('ui_ultrasonic.html'), 'ultrasonic'))
            turbo.push(turbo.replace(render_template('ui_voltage.html'), 'battery'))
            turbo.push(turbo.replace(render_template('ui_mpu.html'), 'mpu'))
            turbo.push(turbo.replace(render_template('ui_servo.html'), 'servo'))


def global_logger(name):
    formatter = logging.Formatter(fmt=LOG_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(handler)
    return custom_logger


if __name__ == '__main__':
    logger = global_logger('root')
    logger.debug('Starting Hexapod webserver')
    app.hexapod = Hexapod.Hexapod()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
