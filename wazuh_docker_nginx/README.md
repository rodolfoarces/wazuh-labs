# Nginx Reverse Proxy for Wazuh - Docker deployment

## Changes to current Docker compose

Changes need to be maed to the `docker-compose.yml` file. Comment the ports that the Nginx Reverse Proxy will manage.

```
wazuh.manager:
...
    ports:
      - "1514:1514"
      - "1515:1515"
      - "514:514/udp"
        #- "55000:55000"
...
wazuh.indexer:
...
      #ports:
      #- "9200:9200"
      #- "9300:9300"
...
wazuh.dashboard:
...
      #ports:
      #- 443:5601
...
```

We need to add the Nginx Service to the `docker-compose.yml`, this service will receive communications on the commented ports.


```
...
wazuh.proxy:
    image: nginx
    hostname: wazuh.proxy
    restart: always
    ports:
      - 443:443
      - 9300:9300
      - 9200:9200
      - 55000:55000
    volumes:
      - ./config/wazuh_indexer_ssl_certs/wazuh.nginx.pem:/etc/ssl/certs/proxy.pem
      - ./config/wazuh_indexer_ssl_certs/wazuh.nginx-key.pem:/etc/ssl/certs/proxy-key.pem
      - ./config/wazuh_indexer_ssl_certs/root-ca-proxy.pem:/etc/ssl/certs/root-ca.pem
      - ./config/wazuh_proxy/wazuhindexer_proxy:/etc/nginx/nginx.conf
    depends_on:
      - wazuh.indexer
      - wazuh.manager
      - wazuh.dashboard
    links:
      - wazuh.indexer:wazuh.indexer
      - wazuh.dashboard:wazuh.dashboard
      - wazuh.manager:wazuh.manager
...
```

The Nginx Proxy will need the configuration file with all backend and fronend definitions `/etc/nginx/nginx.conf`.

```
events {}

http {
	server {

		listen 80 default_server;
		listen [::]:80 default_server;
		rewrite     ^   https://$server_name$request_uri? permanent;
	}
}

stream {
	upstream wazuhmanager {
		server wazuh.manager:55000;
	}
	upstream wazuhdashboard {
		server wazuh.dashboard:5601;
	}

	upstream wazuhindexer-transport {
		server wazuh.indexer:9300;
	}
	upstream wazuhindexer-http {
		server wazuh.indexer:9200;
	}

    server {
        listen 9300;
        ssl_certificate /etc/ssl/certs/proxy.pem;
        ssl_certificate_key /etc/ssl/certs/proxy-key.pem;
        ssl_trusted_certificate /etc/ssl/certs/root-ca.pem;
        proxy_pass wazuhindexer-transport;
        ssl_preread on;
    }
    server {
        listen 9200;
        listen [::]:9200;
        ssl_certificate /etc/ssl/certs/proxy.pem;
        ssl_certificate_key /etc/ssl/certs/proxy-key.pem;
        ssl_trusted_certificate /etc/ssl/certs/root-ca.pem;
        proxy_pass wazuhindexer-http;
        ssl_preread on;
    }

    server {
        listen 55000;
        listen [::]:55000;
        ssl_certificate /etc/ssl/certs/proxy.pem;
        ssl_certificate_key /etc/ssl/certs/proxy-key.pem;
        ssl_trusted_certificate /etc/ssl/certs/root-ca.pem;
        proxy_pass wazuhmanager;
        ssl_preread on;
    }

    server {
        listen 443;
        listen [::]:443;
        ssl_certificate /etc/ssl/certs/proxy.pem;
        ssl_certificate_key /etc/ssl/certs/proxy-key.pem;
        ssl_trusted_certificate /etc/ssl/certs/root-ca.pem;
        proxy_pass wazuhdashboard;
        ssl_preread on;
    }
}
```

## Cross-Cluster Search (MSSP) Integrations

This Nginx approach allows us to connect to the Wazuh Indexer from a CCS/MSSP node.

The CCS/MSSP certificate must be trusted by the Wazuh Indexer, you can use the  `root-ca.pem` and  `root-key.pem` to generate the certificate files for all servers.

The certificate definition is added to the Wazuh Indexer configurations.

```
...
plugins.security.nodes_dn:
- "CN=wazuh.indexer,OU=Wazuh,O=Wazuh,L=California,C=US"
- "CN=mssp,OU=Wazuh,O=Wazuh,L=California,C=US"
plugins.security.restapi.roles_enabled:
...
```

When configuring the CCS/MSSP communication, you can do it using the remote cluster proxy mode.

```
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "indexer": {
          "mode": "proxy",
          "proxy_address": "<DOCKER_HOST_IP>:9300"
        }
      }
    }
  }
}
```