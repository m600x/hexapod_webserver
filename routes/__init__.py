from flask import Blueprint
routes = Blueprint('routes', __name__)

from .adc import *
from .buzzer import *
from .led import *
from .mpu import *
from .servo import *
from .ultrasonic import *