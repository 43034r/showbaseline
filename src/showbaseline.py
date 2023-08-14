import json
import os
import datetime
import schedule
import time
import requests
import random
import threading

DT_API_TOKEN = os.getenv('DT_API_TOKEN', default='dt0c01.X.X')
DT_API_URL = os.getenv('DT_API_URL', default='https://provide-API-URL-WITH-END/api/v1')
SVC_LISTSTR = os.getenv( 'SVC_LIST', default="SERVICE-F531D98ABDEE9F9D, SERVICE-2F612B9CB96EF167")
LOG_LEVEL:int = os.getenv('LOG_LEVEL', default=0) 
UPDATE_INTERVAL:int = os.getenv('UPDATE_INTERVAL', default=5) # in minutes
A_SEND_MINMAX:int = os.getenv('A_SEND_MINMAX', default=0) # send min\max or only median
A_SEND_COUNT:int = os.getenv('A_SEND_COUNT', default=0)  # send count or not 0 - not, 1 - yes.
SVC_LISTSTR = SVC_LISTSTR.replace(" ", "")
SVC_LIST = SVC_LISTSTR.split(',')

def main_work():
	try:
		print("baseline-detector: Start run - main work")
		get_data_svc()
	except:
		print ("baseline-detector: *** Error")

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
	if LOG_LEVEL == 0: 
		print ("baseline-detector *** DEBUG start PayLoad -->  ")
		print (payload)
		print ("baseline-detector *** DEBUG stop PayLoad -->  ")
	r = requests.post(DT_API_URL + '/entity/infrastructure/custom/baseline-detector?Api-Token=' + DT_API_TOKEN, json=payload, verify=False);
	m = r.text
	if LOG_LEVEL == 0: 
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r)
		print ("baseline-detector *** DEBUG Response -->  ", end='')
		print(m)

def get_data(serviceid):
	global A_SEND_MINMAX
	print ("baseline-detector *** DEBUG start get_data for --> ", serviceid)
	
	firsttime=int(time.time()) 
	secondtime=int(time.time() + 1800)
	r = requests.get(DT_API_URL + '/timeseries/com.dynatrace.builtin%3Aservice.responsetime?includeData=true&aggregationType=MEDIAN&startTimestamp=' + str(firsttime) + '&endTimestamp=' + str(secondtime) + '&predict=true&relativeTime=30mins&entity=' + serviceid + '&Api-Token=' + DT_API_TOKEN, verify=False);
	m = r.text
	if LOG_LEVEL == 0:
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r)
		print ("baseline-detector *** DEBUG response -->  ", end='')
		print(m)
		print(firsttime,"---->",secondtime)
	todo = json.loads(r.text)
	print (todo["dataResult"]["dataPoints"][serviceid])
	for tstring in todo["dataResult"]["dataPoints"][serviceid]:
		threads3 = []
		try:
			print("baseline-detector: *** INFO - thread for ", tstring)
			thread2 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[1], serviceid, 'MED', tstring[0],))
			threads3.append(thread2)
			if A_SEND_MINMAX == 1:
				thread3 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[2], serviceid, 'MIN', tstring[0],))
				threads3.append(thread3)
				thread4 = threading.Thread(target=send_to_dyna, args=('custom:service.resp0nsetime.baseline', tstring[3], serviceid, 'MAX', tstring[0],))
				threads3.append(thread4)
			thread2.start()
			if A_SEND_MINMAX == 1:	
				thread3.start()
				thread4.start()
		except Exception as e: 
			print(e)
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		except:
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		print("baseline-detector: *** INFO - stop get_data_svc")


def get_data_rpm(serviceid):
	global A_SEND_MINMAX
	print ("baseline-detector *** DEBUG start get_data_rpm for --> ", serviceid)
	
	firsttime=int(time.time()) 
	secondtime=int(time.time() + 1800)
	r = requests.get(DT_API_URL + '/timeseries/com.dynatrace.builtin%3Aservice.requestspermin?includeData=true&aggregationType=COUNT&startTimestamp=' + str(firsttime) + '&endTimestamp=' + str(secondtime) + '&predict=true&relativeTime=30mins&entity=' + serviceid + '&Api-Token=' + DT_API_TOKEN, verify=False);
	m = r.text
	if LOG_LEVEL == 0:
		print ("baseline-detector *** DEBUG Response code -->  "  , end='')
		print(r)
		print ("baseline-detector *** DEBUG response -->  ", end='')
		print(m)
		print(firsttime,"---->",secondtime)
	todo = json.loads(r.text)
	print (todo["dataResult"]["dataPoints"][serviceid])
	for tstring in todo["dataResult"]["dataPoints"][serviceid]:
		threads2 = []
		try:
			print("baseline-detector: *** INFO - thread for ", tstring)
			thread2 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[1], serviceid, 'AVG', tstring[0],))
			threads2.append(thread2)
			if A_SEND_MINMAX == 1:
				thread3 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[2], serviceid, 'MIN', tstring[0],))
				threads2.append(thread3)
				thread4 = threading.Thread(target=send_to_dyna, args=('custom:service.requests.baseline', tstring[3], serviceid, 'MAX', tstring[0],))
				threads2.append(thread4)
			thread2.start()
			if A_SEND_MINMAX == 1:	
				thread3.start()
				thread4.start()
		except Exception as e: 
			print(e)
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		except:
			print ("baseline-detector: *** Error get_send_to_dyna() - ", serviceid)
		print("baseline-detector: *** INFO - stop get_data_svc")

def get_data_svc():
	global A_SEND_COUNT
	print("baseline-detector: *** INFO - Start get_data_svc")
	try:
		threads = []
		for element in SVC_LIST:
			print("baseline-detector: *** INFO - thread for ", element)
			thread = threading.Thread(target=get_data, args=(element,))
			threads.append(thread)
			thread.start()
			thread_rpm = threading.Thread(target=get_data_rpm, args=(element,))
			threads.append(thread_rpm)
			print("baseline-detector: *** A_SEND_COUNT", A_SEND_COUNT)
			print("baseline-detector: *** A_SEND_COUNT", A_SEND_COUNT)
			print("baseline-detector: *** A_SEND_COUNT", A_SEND_COUNT)
			if A_SEND_COUNT == 1: 
				thread_rpm.start()
				print("baseline-detector: *** A_SEND_COUNT!", A_SEND_COUNT)
				print("baseline-detector: *** A_SEND_COUNT!", A_SEND_COUNT)
				print("baseline-detector: *** A_SEND_COUNT!", A_SEND_COUNT)
	except Exception as e: print(e)
	except:
		print ("baseline-detector: *** Error get_data_svc()")
	print("baseline-detector: *** INFO - stop get_data_svc")


print ("baseline-detector: *** INFO -- starting...")

try:
	main_work()
except:
	print ("baseline-detector: *** Error 1 main_work")

print ("baseline-detector: *** INFO - Updating tasks...")
schedule.every(UPDATE_INTERVAL).minutes.do(main_work)
print(f'baseline-detector: Scheduled in {UPDATE_INTERVAL} minutes for {SVC_LIST}')

while True:
    schedule.run_pending()
    time.sleep(1)










