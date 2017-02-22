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
	request_key = 'cf457ff56d7ae949f6b28b8d5faf770b'
	domain = 'Dental'
	
	speech = ""
	
	# get api data
	today = ( datetime.datetime.utcnow() - datetime.timedelta(hours = 8) ).strftime("%Y/%m/%d")
	todayCardData = []
	monthCardData = []
	if(request_key):
		if req.get("result").get("action") == 'morning_report':
			speech = "MR reporting"
			
			#url2  = 'https://api.sikkasoft.com/v2/sikkanet_cards/Morning%20Report?request_key='+request_key+'&startdate='+today+'&enddate='+today
			#html2 = urlopen(url2)
        		#response = json.load(html2)
			
			morning_report_json = '{"KPIData": [{"Value": [{"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Scheduled Production", "value": 2535, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$2,535"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Sch Production for Rest of month", "value": 24806, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$24,806"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Month to date New Patients", "value": 27, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "27"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Month to date patients seen", "value": 333, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "333"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Month to date collection", "value": 72440.32, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$72,440"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays new patients", "value": 0, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "0"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "month to date production", "value": 93475, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$93,475"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Todays patients going inactive", "value": 2, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "2"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays patient pending treatment plan", "value": 4, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "4"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Scheduled Appointment", "value": 15, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "15"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays patient pending balance", "value": 6, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "6"}], "Key": "Actual"}], "KPIInfo": {"KPIName": "Morning Report", "ChartType": ["$", "$", "#", "#", "$", "#", "$", "#", "#", "#", "#"], "InitialTabs": "", "KPIType": ["Column"]}}'
			response = json.loads(morning_report_json)
			
			if(response['KPIData']):
				for idx, record in enumerate(response['KPIData'][0]['Value']):
					colName, valType, val = record['ColName'] , response['KPIInfo']['ChartType'][idx] , record['value']
					colName = re.sub(r'# of|#', 'Number of', colName) if '#' in colName else colName
					colName = re.sub(r'Sch ', 'Scheduled ', colName) if 'Sch' in colName else colName
					colName = re.sub(r'patient ', 'patients ', colName, re.I)
					colName = re.sub(r'appointment ', 'appointments ', colName, re.I)					
					valType = re.sub('#', '', valType) if '#' in valType else valType
					if valType == "$":
						val=int(math.ceil(val))
					if 'month' in colName.lower():
						colName = re.sub( r'month to date', '', colName, flags=re.I )
						monthCardData.append([colName.strip().capitalize(), valType, val])
					else:
						colName = re.sub( r'todays', '', colName, flags=re.I )
						todayCardData.append([colName.strip().capitalize(), valType, val])
				if todayCardData:
					speech = 'Todays morning report is as follows...'+'\n' + ". \n".join( [str(colName) + " is " + str(valType) + str(val)  for colName, valType, val in todayCardData] )
					speech = speech + ". Would you like to hear the month to date metrics of your practice?"
				
		elif req.get("result").get("action") == 'morning_report_continue':
			
			morning_report_json = '{"KPIData": [{"Value": [{"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Scheduled Production", "value": 2535, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$2,535"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Sch Production for Rest of month", "value": 24806, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$24,806"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Month to date New Patients", "value": 27, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "27"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Month to date patients seen", "value": 333, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "333"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "Month to date collection", "value": 72440.32, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$72,440"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays new patients", "value": 0, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "0"}, {"avg": 17603.938181818183, "Regionalavg": "$17,604", "ColName": "month to date production", "value": 93475, "total": 193643.32, "RegionalTotal": "$193,643", "RegionalValue": "$93,475"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Todays patients going inactive", "value": 2, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "2"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays patient pending treatment plan", "value": 4, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "4"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "Scheduled Appointment", "value": 15, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "15"}, {"avg": 17603.938181818183, "Regionalavg": "17,604", "ColName": "todays patient pending balance", "value": 6, "total": 193643.32, "RegionalTotal": "193,643", "RegionalValue": "6"}], "Key": "Actual"}], "KPIInfo": {"KPIName": "Morning Report", "ChartType": ["$", "$", "#", "#", "$", "#", "$", "#", "#", "#", "#"], "InitialTabs": "", "KPIType": ["Column"]}}'
			response = json.loads(morning_report_json)			
			if(response['KPIData']):
				for idx, record in enumerate(response['KPIData'][0]['Value']):
					colName, valType, val = record['ColName'] , response['KPIInfo']['ChartType'][idx] , record['value']
					colName = re.sub(r'# of|#', 'Number of', colName) if '#' in colName else colName
					colName = re.sub(r'Sch ', 'Scheduled ', colName) if 'Sch' in colName else colName
					colName = re.sub(r'patient ', 'patients ', colName, re.I)
					colName = re.sub(r'appointment ', 'appointments ', colName, re.I)					
					valType = re.sub('#', '', valType) if '#' in valType else valType
					if valType == "$":
						val=int(math.ceil(val))
					if 'month' in colName.lower():
						colName = re.sub( r'month to date', '', colName, flags=re.I )
						monthCardData.append([colName.strip().capitalize(), valType, val])
					else:
						colName = re.sub( r'todays', '', colName, flags=re.I )
						todayCardData.append([colName.strip().capitalize(), valType, val])
				if monthCardData:
					speech = 'Your month to date practice metrics are as follows...'+'\n' + ". \n".join( [str(colName) + " is " + str(valType) + str(val)  for colName, valType, val in monthCardData] )

				
		elif req.get("result").get("action") == 'appointments':
			speech = "AP reporting"

			#url3  = 'https://api.sikkasoft.com/v2/appointments?request_key='+request_key+'&startdate='+today+'&enddate='+today+'&sort_order=asc&sort_by=appointment_time&fields=patient_name,time,type,guarantor_name,length'
			#html3 = urlopen(url3)
        		#response = json.load(html3)
			
			appointments_json = '[{"total_count": "15", "items": [{"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/2110"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "2110", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/78468", "time": "08:30", "patient_name": "Cruz Janet", "appointment_sr_no": "78468"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7222"}, "type": "ORTHO", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7222", "length": "80", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/83876", "time": "08:30", "patient_name": "Ramon Carolynn", "appointment_sr_no": "83876"}, {"provider_id": "JB", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/6206"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/JB"}, "guarantor_name": "", "practice_id": "1", "patient_id": "6206", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/80979", "time": "09:30", "patient_name": "Cooper Melvin", "appointment_sr_no": "80979"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/1046"}, "type": "ADJUSTMENT", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "1046", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84225", "time": "09:50", "patient_name": "Palmer Joe", "appointment_sr_no": "84225"}, {"provider_id": "JB", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/6154"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/JB"}, "guarantor_name": "", "practice_id": "1", "patient_id": "6154", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/81870", "time": "10:30", "patient_name": "Jackson Clark", "appointment_sr_no": "81870"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7493"}, "type": "ORTHO", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7493", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84147", "time": "10:50", "patient_name": "Henderson Lucia", "appointment_sr_no": "84147"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/341"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "341", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/81849", "time": "11:30", "patient_name": "Gonzales Jacquelynn", "appointment_sr_no": "81849"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7797"}, "type": "DELIVERY", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7797", "length": "40", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84361", "time": "11:50", "patient_name": "Langford Courtney", "appointment_sr_no": "84361"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/6551"}, "type": "CONSULTATION", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "6551", "length": "30", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84446", "time": "12:30", "patient_name": "Phillips Arthur", "appointment_sr_no": "84446"}, {"provider_id": "JB", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/6548"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/JB"}, "guarantor_name": "", "practice_id": "1", "patient_id": "6548", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/77603", "time": "14:00", "patient_name": "Rausch Sherri", "appointment_sr_no": "77603"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7520"}, "type": "ORTHO", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7520", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/82917", "time": "14:00", "patient_name": "Junker Tomasa", "appointment_sr_no": "82917"}, {"provider_id": "10", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7191"}, "type": "FILLING", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/10"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7191", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84158", "time": "14:00", "patient_name": "Godfrey Edward", "appointment_sr_no": "84158"}, {"provider_id": "2", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/1993"}, "type": "FILLING", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/2"}, "guarantor_name": "", "practice_id": "1", "patient_id": "1993", "length": "80", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/7407", "time": "15:00", "patient_name": "Treat Joan", "appointment_sr_no": "7407"}, {"provider_id": "113", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/6955"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/113"}, "guarantor_name": "", "practice_id": "1", "patient_id": "6955", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84510", "time": "15:00", "patient_name": "Howard Patricia", "appointment_sr_no": "84510"}, {"provider_id": "113", "practice": {"href": "https://api.sikkasoft.com/v2/practices/1"}, "patient": {"href": "https://api.sikkasoft.com/v2/practices/1/patients/7673"}, "type": "Prophy Appointment", "provider": {"href": "https://api.sikkasoft.com/v2/practices/1/providers/113"}, "guarantor_name": "", "practice_id": "1", "patient_id": "7673", "length": "60", "href": "https://api.sikkasoft.com/v2/practices/1/appointments/84501", "time": "16:00", "patient_name": "Mills Oscar", "appointment_sr_no": "84501"}], "limit": "500", "offset": "0"}]' 
			response = json.loads(appointments_json)
			
			if(response):
				index = 1
				count = 0
				first = 0
				patient_name = ""
				current_time = (datetime.datetime.utcnow() - datetime.timedelta(hours = 8)).strftime('%H:%M:%S')
				current_time = datetime.datetime.strptime(current_time, '%H:%M:%S')
				total_apmnt = response[0]['total_count']
				if (int(total_apmnt) > 0):
					first_apmnt = response[0]['items'][1]['time']
					first_apmnt = datetime.datetime.strptime(first_apmnt, "%H:%M")
					last_apmnt = response[0]['items'][int(total_apmnt)-1]['time']
					last_apmnt = datetime.datetime.strptime(last_apmnt, "%H:%M")
					if  current_time < first_apmnt:
						first_apmnt = first_apmnt.strftime("%I:%M %p")
						patient_name = response[0]['items'][1]['patient_name']
						speech = "Today you have "+str(total_apmnt)+" appointments. Your first patient, " + patient_name +"... will arrive at "+first_apmnt+" and your last appointment is at " + last_apmnt.strftime("%I:%M %p")+"."
					else:
						if(current_time > last_apmnt ):
							speech = "You have no appointments for the day."
						else:
							while(index  < int(total_apmnt) ):
								apmnt = response[0]['items'][index]['time']
								apmnt = datetime.datetime.strptime(apmnt, "%H:%M") 
								if apmnt > current_time:
									if first == 0:
										first_apmnt = apmnt
										first = 1
										patient_name = response[0]['items'][index]['patient_name']
									count = count+1
								index = index +1
							first_apmnt = first_apmnt.strftime("%I:%M %p")
							speech = "You have "+str(count)+" appointments remaining for the day. Your next patient, " + patient_name +"... will arrive at "+first_apmnt+". Your last appointment is at " + last_apmnt.strftime("%I:%M %p")+"."
				else:
					speech = "You have no scheduled appointments today."


	return {
	 	"speech":speech,
	 	"displayText":speech,
	 	"source":"apiai-dental"
	 }
	
if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000)) # flask is on 5000

	print "Starting app om port %d", port
	
	app.run(debug=True, port=port, host='0.0.0.0')
