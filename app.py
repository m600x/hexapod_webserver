#!/usr/bin/env python3
# coding:utf-8

import os
import time
import logging
import threading
from turbo_flask import Turbo
from flask import Flask, render_template
from Hexapod import Hexapod

LOG_FORMAT = "[%(asctime)s][ %(levelname)-8s ][ %(module)s:%(lineno)s ] %(message)s"
app = Flask(__name__)
turbo = Turbo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/ultrasonic')
def ultrasonic():
    return {'ultrasonic': hexapod.ultrasonic.get_distance()}


@app.route('/api/buzzer')
def buzzer():
    hexapod.buzzer.toggle()
    return {'buzzer': hexapod.buzzer.status_buzzer}


@app.route('/api/buzzer/<time_ms>')
def buzzer_ms(time_ms):
    hexapod.buzzer.active_ms(time_ms)
    return {'buzzer': hexapod.buzzer.status_buzzer}


@app.route('/api/adc/1')
def battery_voltage1():
    return {'battery1': hexapod.adc.get_battery_1_voltage()}


@app.route('/api/adc/2')
def battery_voltage2():
    return {'battery2': hexapod.adc.get_battery_2_voltage()}


@app.route('/api/mpu')
def mpu():
    pitch, roll, yaw = hexapod.mpu.get_mpu()
    return {'pitch': pitch,
            'roll': roll,
            'yaw': yaw}


@app.route('/api/led/rainbow')
def led_rainbow():
    hexapod.led.rainbow()
    return "Rainbow"


@app.context_processor
def inject_load():
    return hexapod.get_sensors()


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_data).start()


def update_data():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('ui_ultrasonic.html'), 'ultrasonic'))
            turbo.push(turbo.replace(render_template('ui_voltage.html'), 'battery'))
            turbo.push(turbo.replace(render_template('ui_mpu.html'), 'mpu'))


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
    hexapod = Hexapod.Hexapod()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
