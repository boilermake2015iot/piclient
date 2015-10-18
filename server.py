from flask import Flask, request
import json
import interpreter
import traceback
import sys
import devices
import RPi.GPIO as GPIO

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def hello():
	try:
		program = json.loads(request.data)
	except ValueError, e:
		print request.data
		return json.dumps({'error': 'invalid json'}), 400
	if "Pages" not in program:
		return json.dumps({'error': 'no pages in program'}), 400
	hasMain = False
	for page in program["Pages"]:
		if 'Name' not in page:
			return json.dumps({'error': 'malformed page'}), 400
		if page['Name'] == 'Main':
			hasMain = True
	if not hasMain:
		return json.dumps({'error': 'no main page'}), 400
	try:
		interpreter.interp(program)
	except:
		print '-'*20
		traceback.print_exc(file=sys.stdout)
		print '-'*20
		return json.dumps({'error': 'problem running program'}), 400
	return json.dumps({'success': 'program ran to completion'}), 200

if __name__ == "__main__":
	devices.setup()
	devices.set_in('Button',devices.Button(16, GPIO.PUD_UP))
	devices.set_in('TempSensor',devices.TemperatureHumiditySensor(7))
	devices.set_out('Servo', devices.Servo(12))
	devices.set_out('RgbLed', devices.RgbLed(11, 13, 15, 100))
	devices.set_out('BlueLed', devices.Led(3,120))
	app.run(host='0.0.0.0', port=80,debug=True)
