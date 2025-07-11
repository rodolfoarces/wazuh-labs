#!/usr/bin/env /var/ossec/framework/python/bin/python3.10
import sys
import json
import requests
from requests.auth import HTTPBasicAuth

# Read configuration parameters
# <hook_url>http://glpi00.wazuh.local</hook_url>
# <api_key>USER_TOKEN:APP_TOKEN</api_key>

# Alert information
alert_file = open(sys.argv[1])
# Connection
user_token = sys.argv[2].split(':')[0]
app_token = sys.argv[2].split(':')[1]
# URLs
session_url =  sys.argv[3] + '/apirest.php/initSession' 
hook_url = sys.argv[3] + '/apirest.php/Ticket/'

# Read the alert file
alert_json = json.loads(alert_file.read())
alert_file.close()

#print (sys.argv)
#print (json.dumps(alert_json))

# Extract issue fields
alert_level = alert_json['rule']['level']
rule_id = alert_json['rule']['id']
subject = alert_json['rule']['description']
agent_id = alert_json['agent']['id']
agent_name = alert_json['agent']['name']

name =  'Agent ID: ' + agent_id + ' Alert Level:' + str(alert_level)
description = '- Rule ID:' + rule_id + '\n- Agent ID:' + agent_id + '\n- Agent Name:' + agent_name + '\n- Description' + subject + '\n- Alert Level:' + str(alert_level)

# Session init
try:
    session_headers = {'Content-type': 'application/json', 'Authorization': ("user_token " + user_token), 'App-Token': app_token }
    # Send the session request
    session = requests.get(session_url, headers=session_headers, verify=False)
    session_token_data = session.content.decode('utf-8')
    #print(session_token_data)
    session_token = json.loads(session_token_data)
except:
    print ("Authentication error")
    sys.exit(1)

# Generate request
## Include the Session
issue_headers = {'Content-type': 'application/json', 'Session-Token': session_token["session_token"] , 'App-Token': app_token }
## Request content
issue_data = {
    "input": {
        "name": name,
        "content": description
    }
    }
# Send the request
try:
    response = requests.post(hook_url, json=issue_data, headers=issue_headers, verify=False)
    #print (response.content.decode('utf-8'))
except:
    print ("Issue creation error")
    sys.exit(1)
sys.exit(0)
