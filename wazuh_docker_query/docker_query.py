#!/usr/bin/python3
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

# Saving information to a local file
def saveToFile(message, local_file):
    logger.debug("Exporting information to : %s" % local_file)
    try:
        f = open(local_file, 'a+')
        f.write(f'{json.dumps(message)}\n')
    except IOError:
        logger.error("Error opening output file")
        exit(3) 

def getContainers(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/containers/json'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/Container
    try:
        containers = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_containers, output_errors = containers.communicate()
        logger.debug(output_containers)
    except Exception as error:
        logger.error('General error: {0}, query error: {1}', error, output_errors)
        exit(1)    
    return (json.loads(output_containers))

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
                saveToFile(msg, local_file)

def getImages(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/images/json'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/Image
    try:
        images = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_images, errors_images = images.communicate()
        logger.debug(output_images)
    except Exception as error:
        logger.error('General error: {0}, query error: {1}', error, errors_images)
        exit(1)    
    return (json.loads(output_images))
    
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
            saveToFile(msg, local_file)

def getVolumes(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/volumes'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/Volume
    try:
        volumes = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_volumes, errors_volumes = volumes.communicate()
        logger.debug(output_volumes)
    except Exception as error:
        logger.error('General error: {0}, query error: {1}', error, errors_volumes)
        exit(1)   
    return (json.loads(output_volumes))           
    
def postVolumes(volumes, local_file = None):
    for volume in volumes:
        msg = { 'service': 'docker', 'docker_volumes': volume }
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
            saveToFile(msg, local_file)

def getVersion(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/version'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/System/operation/SystemVersion
    try:
        version = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_version, errors_version = version.communicate()
        logger.debug(output_version)
    except Exception as error:
        logger.error('General error: {0}, query error: {1}', error, errors_version)
        exit(1)      
    return (json.loads(output_version))

def postVersion(version, local_file = None):
    msg = { 'service': 'docker', 'docker_version': version }
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
        saveToFile(msg, local_file)
            
def getInfo(docker_socket_file = '/var/run/docker.sock', docker_socket_query = 'http://localhost/info'):
    # https://docs.docker.com/reference/api/engine/version/v1.48/#tag/System/operation/SystemInfo
    try:
        info = subprocess.Popen(['/usr/bin/curl', '--unix-socket', docker_socket_file , docker_socket_query] ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_info, errors_info = info.communicate()
        logger.debug(output_info)
    except Exception as error:
        logger.error('General error: {0}, query error: {1}', error, errors_info)
        exit(1)   
    return (json.loads(output_info))

def postInfo(info, local_file = None):
    msg = { 'service': 'docker', 'docker_info': info }
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
        saveToFile(msg, local_file)
                          
if __name__ == "__main__":
    # Read parameters using argparse
    ## Initialize parser
    parser = argparse.ArgumentParser()
    ## Adding optional argument
    parser.add_argument("-c", "--containers", help = "Obtain running container list", action="store_true")
    parser.add_argument("-i", "--images", help = "Obtain running container list", action="store_true")
    parser.add_argument("-v", "--volumes", help = "Obtain volumes list", action="store_true")
    parser.add_argument("-V", "--docker-version", help = "Obtain software version", action="store_true")
    parser.add_argument("-I", "--docker-info", help = "Obtain system information", action="store_true")
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
            r = open(args.local, 'a+')
            r.close()
            local_file = args.local
        except IOError:
            logger.error("Error opening local file")
            exit(3)
    else:
        local_file = None
        
    if args.containers:
        #getContainers()
        #postContainers(local_file=local_file)
        postContainers(getContainers(),local_file=local_file)
    
    if args.images:
        #getImages()
        #postImages(local_file=local_file)
        postImages(getImages(), local_file=local_file)

    if args.volumes:
        #getVolumes()
        #postVolumes(local_file=local_file)
        postVolumes(getVolumes(), local_file=local_file)
    
    if args.docker_version:
        #getVersion()
        #postVersion(local_file=local_file)
        postVersion(getVersion(), local_file=local_file)
        
    if args.docker_info:
        #getInfo()
        #postInfo(local_file=local_file)
        postInfo(getInfo(), local_file=local_file)