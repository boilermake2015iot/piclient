from interpreter import *
import devices
import RPi.GPIO as GPIO
from time import sleep

devices.setup()

devices.set_in('TempSensor',devices.TemperatureHumiditySensor(7))

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'CurrentTemperature', 'Device': 'TempSensor'}}]}]})
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'CurrentHumidity', 'Device': 'TempSensor'}}]}]})

"""
devices.set_out('RedLed', devices.Led(12, 120))
devices.set_in('Button', devices.Button(8, GPIO.PUD_UP))
devices.set_out('Servo', devices.Servo(11))

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 5}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'If', 'Condition': {'Type': 'Expression', 'Op': '>', 'Left': {'Type': 'Constant', 'Value': 5}, 'Right': {'Type': 'Constant', 'Value': 4}}, 'Page': 'Sub'}, {'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK2'}}]}, {'Name': 'Sub', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK'}}]}]})
sleep(2)
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle': {'Type': 'Constant', 'Value': 45} }]}]})
sleep(2)
#interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'WaitButtonPress', 'Device': 'Button'}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle':{'Type': 'Constant', 'Value': -45}}]}]})
sleep(2)
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'LedSet', 'Device': 'RedLed', 'Value': {'Type': 'Constant', 'Value': True}}]}]})

#time.sleep(5)
"""
devices.cleanup()
