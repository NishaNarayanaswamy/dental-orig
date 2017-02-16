import urllib
import json
import os

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
	if req.get("result").get("action") != 'shipping.cost':
		return {}
	result = req.get("result")
	parameters = result.get("parameters")
	zone = parameters.get("shipping-zone")

	# define dictionary/database for cost
	cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

	#speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
	speech = "hahaha blah"

	print("Response:")
	print(speech)

	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-onlinestore-shipping"
	 }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')

	
