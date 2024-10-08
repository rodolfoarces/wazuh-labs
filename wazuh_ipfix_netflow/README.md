# IPFix or NetFlow Collection and Wazuh ingestion

## Rationale

Deploy a IPFix/NetFlow collector service. Ingest data and output to a Wazuh Agent readable format.

## Collector installation

For the collector software, we propose the usage of [IpFixCol2](https://github.com/CESNET/ipfixcol2) that provides an extensible platform and already present protocol ingestion and JSON output. 

### Installing pre-requisites

The software requires an additional library [libfds](https://github.com/CESNET/libfds), provided by the same organization.

To install this library, you'll have to install additional software en libraries to compile

```
apt install gcc g++ cmake make libxml2-dev liblz4-dev libzstd-dev doxygen pkg-config
```

Follow the documentation in [project site](https://github.com/CESNET/libfds#how-to-build)


## Compiling the collector

To install the software, follow the documentation in the [project site](https://github.com/CESNET/ipfixcol2?#how-to-build)

## Running the collector

Using the provided [test examples](https://raw.githubusercontent.com/CESNET/ipfixcol2/refs/heads/master/doc/data/configs/t2anon2json.xml), to run the collector, execute the following command

```
/usr/local/bin/ipfixcol2 -c tcp2anon2json.xml
```

## Testing

2 configuration files were used to execute the service, one listening on TCP and another on UDP, the files are added to this project's directory

```
/usr/local/bin/ipfixcol2 -c ./tcp2json.xml &
/usr/local/bin/ipfixcol2 -c ./udp2json.xml &
```

**testing TCP IPFIX**

The software provides a data flow creation tool to test the collector and its configurations. The example flow is included in the projects _doc_ directory.

```
 ipfixsend2 -d 10.1.1.152 -p 4739 -t TCP -i ./ipfixcol2/doc/data/ipfix/example_flows.ipfix -n -R 1.0
```

**testing UDP NetFlow**

The [nflow-generator project](https://github.com/nerdalert/nflow-generator)  provides a way to generate random netflow data in UDP.

Per the project documentation, a container is launched with the collector information

```
docker run -it --rm networkstatic/nflow-generator -t 10.1.1.152 -p 4739
```
