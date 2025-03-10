import json
import subprocess
import argparse
import logging
from pathlib import Path
from socket import AF_UNIX, SOCK_DGRAM, socket

location = 'agent-queue'
WAZUH_SOCKET = f'/var/ossec/queue/sockets/queue'

## Logging options
# https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
# create file handler which logs even debug messages
logger = logging.getLogger("docker-report")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.INFO)
fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

def getContainers(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/containers/json'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/Container
    try:
        containers = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = containers.communicate()
        r = json.loads(output)
        #print(str(r))
    except Exception as error:
        logger.error('General error: {0}', error)
        exit(1)
        
    return (containers)

def postContainers(containers, local_file = None):
    for container in containers:
        if container["State"] == 'running':
            msg = { 'service': 'docker', 'docker_container': container }
            # Default action is to send information via agent/socket
            if local_file == None: 
                string = '1:{0}->docker:{1}'.format(location, json.dumps(msg))
                try:
                    sock = socket(AF_UNIX, SOCK_DGRAM)
                    sock.connect(WAZUH_SOCKET)
                    sock.send(string.encode())
                    sock.close()
                except FileNotFoundError:
                    logger.error('# Error: Unable to open socket connection at %s' % WAZUH_SOCKET)
                    exit(2)
            # Alternativa option is to save it to a file
            else:
                logger.debug("Saving containers information to : %s" % local_file)
                try:
                    f = open(local_file, 'a+')
                    f.write(msg)
                except IOError:
                    logger.error("Error opening output file")
                    exit(3)

def getImages(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/images/json'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/Image
    try:
        images = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = images.communicate()
        r = json.loads(output)
        #print(str(r))
    except Exception as error:
        logger.error('General error: {0}', error)
        exit(1)
        
    return (images)            
    
def postImages(images, local_file = None):
    for image in images:
        msg = { 'service': 'docker', 'docker_image': image }
        # Default action is to send information via agent/socket
        if local_file == None: 
            string = '1:{0}->docker:{1}'.format(location, json.dumps(msg))
            try:
                sock = socket(AF_UNIX, SOCK_DGRAM)
                sock.connect(WAZUH_SOCKET)
                sock.send(string.encode())
                sock.close()
            except FileNotFoundError:
                logger.error('# Error: Unable to open socket connection at %s' % WAZUH_SOCKET)
                exit(2)
        # Alternativa option is to save it to a file
        else:
            logger.debug("Saving containers information to : %s" % local_file)
            try:
                f = open(local_file, 'a+')
                f.write(msg)
            except IOError:
                logger.error("Error opening output file")
                exit(3)
                          
if __name__ == "__main__":
    # Read parameters using argparse
    ## Initialize parser
    parser = argparse.ArgumentParser()
    ## Adding optional argument
    parser.add_argument("-c", "--containers", help = "Obtain running container list", action="store_true")
    parser.add_argument("-i", "--images", help = "Obtain running container list", action="store_true")
    parser.add_argument("-l", "--local", help = "Use local file to store events", action="store")
    parser.add_argument("-o", "--output", help = "Log output to file")
    parser.add_argument("-D", "--debug", help = "Enable debug", action="store_true")
    #parser.add_argument("-l", "--local", help = "Use local file to store events, requires: -d DIR|FILE", action="store")
    ## Read arguments from command line
    args = parser.parse_args()
    
    ## Log to file or stdout
    # https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
    # create file handler which logs even debug messages
    logger = logging.getLogger("docker-output")
    
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # If output file is set, all messages go there
    if args.output:
        # create console handler with a higher log level
        fh = logging.FileHandler(args.output)
        # Define log level
        if args.debug == True:
            fh.setLevel(logging.DEBUG)
            fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            fh.setLevel(logging.INFO)
            fh_formatter = logging.Formatter('%(message)s')
        
        fh.setFormatter(fh_formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
    else:
        # create console handler with a higher log level
        fh = logging.StreamHandler()
        # Define log level
        if args.debug == True:
            fh.setLevel(logging.DEBUG)
            fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            fh.setLevel(logging.INFO)
            fh_formatter = logging.Formatter('%(message)s')
        
        fh.setFormatter(fh_formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        
    if args.local:
        try:
            # testing if the script can access the local file
            local_file = open(args.local, 'a+')
            local_file.close()
        except IOError:
            logger.error("Error opening local file")
            exit(3)
    else:
        local_file = None
        
    if args.containers:
        getContainers()
        postContainers(local_file=local_file)
    
    if args.images:
        getImages()
        postImages(local_file=local_file)