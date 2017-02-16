import urllib
import json
import os
import urllib2
from urllib2 import urlopen
from flask import Flask
from flask import request
from flask import make_response

# start app in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print('Request:')
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):
	
	speech = "hello Sikka"

	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-dental"
	 }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')

	