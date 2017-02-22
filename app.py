import urllib
import json
import os
import urllib2
from urllib2 import urlopen
import time
import datetime
import re
import math
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
	
	# demo account login - use manual request key everyday
	#login_url= 'https://api.sikkasoft.com/auth/v2/provider_accounts?un=ddemo2&pw=$Sikka4040&app_id=cf345eef7cb42a39cff6972d57fe6149&app_key=8003044355153fe930ec82ca091e334e&encrypted=false&device_id=fOinX6aGKzc:APA91bHer7V6YQM5re379jNRlc4fnXBmo3ElTB0ivPgINJ76HURuabkzKXmXFZ2ITk9yBFHHDu3dCbq2s8RcuDhWdqyC8BYSAdajjp8ep3TaC_T8k4dHZJZJ-cDeH0NU6ZRjOY1O6ljb&device_type=android'
	#html = urlopen(login_url)
	#login_response = json.load(html)
	#request_key = login_response['profiles'][0]['request_key']
	#domain = login_response['profiles'][0]['profile_type']
	request_key = '952bce8b73d55ca2a6715c1520c80b2a'
	domain = 'Dental'
	
	speech = ""
	
	# get api data
	today = ( datetime.datetime.utcnow() - datetime.timedelta(hours = 8) ).strftime("%Y/%m/%d")
	todayCardData = []
	monthCardData = []
	if(request_key):
		if req.get("result").get("action") == 'morning_report':
			speech = "Today's morning report is as follows... Scheduled production is $2535. New patients is 0. Patients going inactive is 2. Patients pending treatment plan is 4. Scheduled appointment is 15. Patients pending balance is 6"
				
		elif req.get("result").get("action") == 'appointments':
			speech = "You have 3 appointments remaining for the day. Your next patient, Howard Patricia... will arrive at 3:00 PM. Your last appointment is at 04:00 PM."
	
	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-dental"
	 }

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')
