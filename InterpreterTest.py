from interpreter import *
import devices
import RPi.GPIO as GPIO
from time import sleep

devices.setup()

devices.set_in('Button',devices.Button(16, GPIO.PUD_UP))
devices.set_in('TempSensor',devices.TemperatureHumiditySensor(7))
devices.set_out('Servo', devices.Servo(12))
devices.set_out('RgbLed', devices.RgbLed(11, 13, 15, 100))
devices.set_out('BlueLed', devices.Led(3,120))
#interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'CurrentTemperature', 'Device': 'TempSensor'}}]}]})
#interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'CurrentHumidity', 'Device': 'TempSensor'}}]}]})

"""
devices.set_out('RedLed', devices.Led(12, 120))
devices.set_in('Button', devices.Button(8, GPIO.PUD_UP))
devices.set_out('Servo', devices.Servo(11))

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 5}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'If', 'Condition': {'Type': 'Expression', 'Op': '>', 'Left': {'Type': 'Constant', 'Value': 5}, 'Right': {'Type': 'Constant', 'Value': 4}}, 'Page': 'Sub'}, {'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK2'}}]}, {'Name': 'Sub', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK'}}]}]})
sleep(2)
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle': {'Type': 'Constant', 'Value': 45} }]}]})
sleep(2)
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'WaitButtonPress', 'Device': 'Button'}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle':{'Type': 'Constant', 'Value': -45}}]}]})
sleep(2)
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'LedSet', 'Device': 'RedLed', 'Value': {'Type': 'Constant', 'Value': True}}]}]})

#time.sleep(5)
"""

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'CurrentTemperature', 'Device': 'TempSensor'}}]}]})
print 'Waiting on button'
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'WaitButtonPress', 'Device': 'Button'}]}]})
print 'Button pressed'
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'LedBlink', 'Device': 'BlueLed', 'NumberOfBlinks': {'Type': 'Constant', 'Value': 7}, 'BlinkInterval': {'Type': 'Constant', 'Value': 1}}]}]})
interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetRgbLed', 'Device': 'RgbLed', 'R': {'Type': 'Constant', 'Value': 255}, 'G': {'Type': 'Constant', 'Value': 102}, 'B': {'Type': 'Constant', 'Value': 0}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle': {'Type': 'Constant', 'Value': 45} }, {'Type': 'Sleep', 'Param':{'Type': 'Constant', 'Value': 5}}]}]})

devices.cleanup()
