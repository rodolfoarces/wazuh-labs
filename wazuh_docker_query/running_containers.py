import sys
import json
import subprocess
import os.path
from socket import AF_UNIX, SOCK_DGRAM, socket

location = 'agent-queue'
WAZUH_SOCKET = f'/var/ossec/queue/sockets/queue'

try:
    containers = subprocess.Popen(['/usr/bin/curl', '--unix-socket', '/var/run/docker.sock', 'http://localhost/containers/json'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, errors = containers.communicate()
    r = json.loads(output)
    #print(str(r))
except Exception as error:
    print('General error: {0}',error)
    exit(1)

for container in r:
    if container["State"] == 'running':
        msg = { 'service': 'docker', 'docker': container }
        #print(json.dumps(container))
        string = '1:{0}->docker:{1}'.format(location, json.dumps(msg))
        print(string)
        try:
            sock = socket(AF_UNIX, SOCK_DGRAM)
            sock.connect(WAZUH_SOCKET)
            sock.send(string.encode())
            sock.close()
        except FileNotFoundError:
            print('# Error: Unable to open socket connection at %s' % WAZUH_SOCKET)
            exit(2)
