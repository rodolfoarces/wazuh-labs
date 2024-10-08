# Wazuh Redmine Integration

## Rationale

Deploy a Redmine instance to forward event information from Wazuh events.

## Deploy redmine

Using the docker compose file

```
docker compose -f ./wazuh-labs/wazuh_redmine/docker-compose-redmine-mysql.yml up -d
```

## Configure Redmine

Enable the redmine REST API

Create a user API key