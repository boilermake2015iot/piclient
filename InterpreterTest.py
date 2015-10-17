from interpreter import *
import devices
import RPi.GPIO as GPIO
devices.setup()

devices.set_out('RedLed', devices.Led(12, 120))
devices.set_in('Button', devices.Button(8, GPIO.PUD_UP))
devices.set_out('Servo', devices.Servo(11))

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 5}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'If', 'Condition': {'Type': 'Expression', 'Op': '>', 'Left': {'Type': 'Constant', 'Value': 5}, 'Right': {'Type': 'Constant', 'Value': 4}}, 'Page': 'Sub'}, {'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK2'}}]}, {'Name': 'Sub', 'Nodes': [{'Type': 'Print', 'Param': {'Type': 'Constant', 'Value': 'OK'}}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle': 45}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'WaitButtonPress', 'Device': 'Button'}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'SetServoAngle', 'Device': 'Servo', 'Angle': -45}]}]})

interp({'Pages': [{'Name': 'Main', 'Nodes': [{'Type': 'LedSet', 'Device': 'RedLed', 'Value': {'Type': 'Constant', 'Value': True}}]}]})

time.sleep(5)

devices.cleanup()
