# Hexapod webserver (Freenove)
Webserver to control Freenove Hexapod Pi

WIP: Only display raw sensor value

## Requirements
- Raspberry Pi
- Python 3

## Currently imported:
- Ultrasonic sensor
- Buzzer
- ADS7830
- MPU6050

### Installation
```shell
python3 -m pip install -r requirements.txt
```

### Run
```shell
python3 app.py
```

## API

### `/api/ultrasonic`
Get the ultrasonic sensor value

### `/api/buzzer`
Toggle the buzzer function

### `/api/buzzer/<time_ms>`
Activate the buzzer for `<time_ms>` in milliseconds (capped to 10seconds)

### `/api/adc/1`
Get the battery 1 voltage level

### `/api/adc/2`
Get the battery 2 voltage level

### `/api/mpu`
Get the MPU6050 reading with Pitch, Roll and Yaw value