#!/usr/bin/env python3
from datetime import datetime
import random
import sys
import time

def getEndpointMessage():
    users = [ 'wazuh-user', 'demo', 'admin']
    endpoints=['/serv-login-service-5.5.0-ann/identity/v1/users/login',
                '/serv-login-service-5.5.0-ann/identity/v1/users?filter=login%20eq%20s',
                '/serv-login-service-5.5.0-ann/identity/v1/authenticator/v1/users/' ]
    endpoint = random.randint(0,2)
    if endpoint == 1:
        user = random.randint(0,2)
        endpoint_url = endpoints[endpoint] + users[user]
    elif endpoint == 2:
        user = random.randint(0,2)
        endpoint_url = endpoints[endpoint] + users[user] + "/status"
    else:
        endpoint_url = endpoints[endpoint]
    endpoint_message = "endpoint:" + endpoint_url
    return endpoint_message

def getLogTime():
    # Date components
    current_datetime = datetime.now()
    log_date = '{:02d}'.format(current_datetime.day) + '/' + '{:02d}'.format(current_datetime.month) + '/' + str(current_datetime.year)
    log_time = '{:02d}'.format(current_datetime.hour) + ":" + '{:02d}'.format(current_datetime.minute) + ":" + '{:02d}'.format(current_datetime.second)
    log_message_time= "RequestDateTime: " + log_date + " " + log_time
    return log_message_time


def getResponseTime(): 
    # Request time components
    response_time = random.randint(50,300)
    response_message= "x-responsetime:" + str(response_time) + ", " + str(response_time) + " ms" 
    return response_message

def addMessage(file):
    try:
        f = open(file, 'a+')
    except IOError:
        print("Error opening log file")
        exit(1)

    f.write(getEndpointMessage() + "\n" + getLogTime() + "\n" + getResponseTime())

file = None

try:
    file = sys.argv[1]
except IndexError:
    print("provided a file")
    exit(2)

while file != None:
    addMessage(file)
    time.sleep(random.randint(2,10))

