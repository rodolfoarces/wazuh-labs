# Docker query script

This script connects to the docker engine API using the docker service socket. It obtains information and fowards it to Wazuh, or stores it in file that can be monitored by the Wazuh Agent

## Command usage
```
usage: docker_query.py [-h] [-a] [-c] [-i] [-v] [-n] [-s] [-m] [-p] [-P] [-N]
                       [-V] [-I] [-l LOCAL] [-o OUTPUT] [-D]

options:
  -h, --help            show this help message and exit
  -a, --all             Obtain all information available
  -c, --containers      Obtain running container list
  -i, --images          Obtain running container list
  -v, --volumes         Obtain volumes list
  -n, --networks        Obtain networks information
  -s, --container-stats
                        Obtain container stats
  -m, --container-mounts
                        Obtain container mounts
  -p, --container-ports
                        Obtain container ports
  -P, --container-processes
                        Obtain container ports
  -N, --container-networks
                        Obtain networks information
  -V, --docker-version  Obtain software version
  -I, --docker-info     Obtain system information
  -l LOCAL, --local LOCAL
                        Use local file to store events
  -o OUTPUT, --output OUTPUT
                        Log output to file
  -D, --debug           Enable debug

```

## Examples

*Example 1*

```
/usr/bin/python3 ./docker_query.py -D -a -o output.log -l info.json
```

Obtains all the information (`-a`) with debug enabled (`-D`).The debug output (`-o`) is saved to file `output.log`, and the information obtained (`-l`) is saved to file `info.json`.
