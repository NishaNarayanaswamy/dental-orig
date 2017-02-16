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

	# login to PM dental
	login_url= 'https://api.sikkasoft.com/auth/v2/provider_accounts?un=ddemo2&pw=$Sikka4040&app_id=cf345eef7cb42a39cff6972d57fe6149&app_key=8003044355153fe930ec82ca091e334e&encrypted=false&device_id=fOinX6aGKzc:APA91bHer7V6YQM5re379jNRlc4fnXBmo3ElTB0ivPgINJ76HURuabkzKXmXFZ2ITk9yBFHHDu3dCbq2s8RcuDhWdqyC8BYSAdajjp8ep3TaC_T8k4dHZJZJ-cDeH0NU6ZRjOY1O6ljb&device_type=android'
    
    try:
        html = urlopen(login_url)
        login_response = json.load(html)
        request_key = login_response['profiles'][0]['request_key']
        session['request_key'] = request_key
        domain = login_response['profiles'][0]['profile_type']
        print request_key
        print domain
    except:
        print("login failed")


	# define dictionary/database for cost
	cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

	speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros. Request key is " + request_key

	#print("Response:")
	#print(speech)

	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-onlinestore-shipping"
	 }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')

	
