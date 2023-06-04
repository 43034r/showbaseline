import json
import datetime
import os
import datetime
import schedule
import time
import requests
import random
from datetime import datetime
import threading

YOUR_DT_API_TOKEN = os.getenv('YOUR_DT_API_TOKEN', 'dt0c01.X.X')
YOUR_DT_API_URL = os.getenv('YOUR_DT_API_URL', 'https://provide-API-URL-WITH-END/api/v1')
YOUR_SVC_LISTSTR = os.getenv( 'YOUR_SVC_LIST', "SERVICE-F531D98ABDEE9F9D, SERVICE-D2E55F5D48FF41A1")
YOUR_LOG_LEVEL:int = os.getenv('YOUR_LOG_LEVEL', 2) 
YOUR_UPDATE_INTERVAL:int = os.getenv('YOUR_UPDATE_INTERVAL', 5) # in minutes
YOUR_A_SEND_MINMAX:int = os.getenv('YOUR_A_SEND_MINMAX', 0) # send min\max or only median
YOUR_A_SEND_COUNT:int = os.getenv('YOUR_A_SEND_COUNT', 0)  # send count or not 0 - not, 1 - yes.
                                  
def main_work():
	try:
		print("baseline-detector: Start run - main work")
		get_data_svc()
	except:
		print ("baseline-detector: *** Error")

def printl(text, *args):
	if int(YOUR_LOG_LEVEL) >= 2: print (text, args)

def printll(text, *args):
	if YOUR_LOG_LEVEL == 1: print (text, args)

def send_to_dyna(timeseriesId, value, svc_to_send, agr, ttime):
	payload = {
		"displayName" : "ShowBaseLine",  
		"listenPorts" : ["9999"],
		"type" : "baseline",
		"favicon" : "https://my.monitoring.wiki/dynatrace/some.png",
		"configUrl" : "https://my.monitoring.wiki/en/dynatrace/showbaseline",
		"tags": ["Baseline", "ShowBaseLine"],
		"properties" : { 
			"dns-name" : "show-base-line.monitoring.wiki", "ip-address" : "172.172.172.172"
			},
			"series" : [
			{ "timeseriesId" : timeseriesId, 
			"dimensions" : { "service" : svc_to_send, "agr" : agr },
			"dataPoints" : [ [ ttime-3300000  , value ] ]
			},
			]
			}
	
	if (value < 0): raise ValueError(f"baseline-detector *** Error {value} < 0")
	if YOUR_LOG_LEVEL == 0: 
		print ("baseline-detector *** DEBUG start PayLoad -->  ")
		print (payload)
		print ("baseline-detector *** DEBUG stop PayLoad -->  ")
	r = requests.post(YOUR_DT_API_URL + '/entity/infrastructure/custom/baseline-detector?Api-Token=' + YOUR_DT_API_TOKEN, json=payload, verify=False);
	m = r.text
	if YOUR_LOG_LEVEL == 0: 
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r);
		print ("baseline-detector *** DEBUG Response -->  ", end='')
		print(m);

def get_data(serviceid):
	printl ("baseline-detector *** DEBUG start get_data for --> ", serviceid)
	
	firsttime=int(time.time()) 
	secondtime=int(time.time() + 1800)
	r = requests.get(YOUR_DT_API_URL + '/timeseries/com.dynatrace.builtin%3Aservice.responsetime?includeData=true&aggregationType=MEDIAN&startTimestamp=' + str(firsttime) + '&endTimestamp=' + str(secondtime) + '&predict=true&relativeTime=30mins&entity=' + serviceid + '&Api-Token=' + YOUR_DT_API_TOKEN, verify=False);
	m = r.text
	if YOUR_LOG_LEVEL == 0:
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r)
		print ("baseline-detector *** DEBUG response -->  ", end='')
		print(m)
		print(firsttime,"---->",secondtime)
	todo = json.loads(r.text)
	printl (todo["dataResult"]["dataPoints"][serviceid])
	for tstring in todo["dataResult"]["dataPoints"][serviceid]:
		threads2 = []
		threads3 = []
		threads4 = []
		try:
			printll("baseline-detector: *** INFO - thread for ", tstring)
			thread2 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[1], serviceid, 'MED', tstring[0],))
			threads2.append(thread2)
			if YOUR_A_SEND_MINMAX == 1:
				thread3 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[2], serviceid, 'MIN', tstring[0],))
				threads3.append(thread3)
				thread4 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[3], serviceid, 'MAX', tstring[0],))
				threads4.append(thread4)
			thread2.start()
			if YOUR_A_SEND_MINMAX == 1:	
				thread3.start()
				thread4.start()
		except Exception as e: 
			print(e)
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		except:
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		printll("baseline-detector: *** INFO - stop get_data_svc")


def get_data_rpm(serviceid):
	printl ("baseline-detector *** DEBUG start get_data_rpm for --> ", serviceid)
	
	firsttime=int(time.time()) 
	secondtime=int(time.time() + 1800)
	r = requests.get(YOUR_DT_API_URL + '/timeseries/com.dynatrace.builtin%3Aservice.requestspermin?includeData=true&aggregationType=COUNT&startTimestamp=' + str(firsttime) + '&endTimestamp=' + str(secondtime) + '&predict=true&relativeTime=30mins&entity=' + serviceid + '&Api-Token=' + YOUR_DT_API_TOKEN, verify=False);
	m = r.text
	if YOUR_LOG_LEVEL == 0:
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r)
		print ("baseline-detector *** DEBUG response -->  ", end='')
		print(m)
		print(firsttime,"---->",secondtime)
	todo = json.loads(r.text)
	printl (todo["dataResult"]["dataPoints"][serviceid])
	for tstring in todo["dataResult"]["dataPoints"][serviceid]:
		threads2 = []
		threads3 = []
		threads4 = []
		try:
			printll("baseline-detector: *** INFO - thread for ", tstring)
			thread2 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[1], serviceid, 'AVG', tstring[0],))
			threads2.append(thread2)
			if YOUR_A_SEND_MINMAX == 1:
				thread3 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[2], serviceid, 'MIN', tstring[0],))
				threads3.append(thread3)
				thread4 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[3], serviceid, 'MAX', tstring[0],))
				threads4.append(thread4)
			thread2.start()
			if YOUR_A_SEND_MINMAX == 1:	
				thread3.start()
				thread4.start()
		except Exception as e: 
			print(e)
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		except:
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		printll("baseline-detector: *** INFO - stop get_data_svc")

def get_data_svc():
	printll("baseline-detector: *** INFO - Start get_data_svc")
	try:
		threads = []
		for element in YOUR_SVC_LIST:
			printll("baseline-detector: *** INFO - thread for ", element)
			thread = threading.Thread(target=get_data, args=(element,))
			threads.append(thread)
			thread.start()
			if YOUR_A_SEND_COUNT == 1:
				thread = threading.Thread(target=get_data_rpm, args=(element,))
				threads.append(thread)
			thread.start()
	except Exception as e: print(e)
	except:
		print ("baseline-detector: *** Error get_data_svc()")
	printll("baseline-detector: *** INFO - stop get_data_svc")


def schedule_next_run():
	time_span = random.randint(1, 15)
	schedule.clear()
	printll(f'"baseline-detector: Scheduled in {time_span} minutes')
	schedule.every(time_span).minutes.do(main_work)


print ("baseline-detector: *** INFO -- starting...")

main_work()

print ("baseline-detector: *** INFO - Updating tasks...")
schedule.every(YOUR_UPDATE_INTERVAL).minutes.do(main_work)
printll(f'baseline-detector: Scheduled in {YOUR_UPDATE_INTERVAL} minutes for {YOUR_SVC_LIST}')

while True:
    schedule.run_pending()
    time.sleep(1)









