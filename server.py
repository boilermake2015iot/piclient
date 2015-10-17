from flask import Flask, request
import json
import interpreter
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
	app.run(host='0.0.0.0', port=80,debug=True)
