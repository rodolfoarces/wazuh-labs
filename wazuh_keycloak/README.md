# Wazuh Keycloack Integration

# Keycloack deployment

Keycloack will require an SSL certificates for the HTTPS communication with the Wazuh Dashboard.

You can create the SSL sets using the [wazuh-certs-tool.sh](https://documentation.wazuh.com/current/user-manual/wazuh-dashboard/certificates.html)

You can deploy Keycloack using docker compose, you can review the [docker-compose.yml](./docker-compose.yml) file. Adjust the *volumes* section to load the SSL certificates and [keycloak.conf](./keycloak.conf) file.

More information in [the official documentation](https://documentation.wazuh.com/current/user-manual/user-administration/single-sign-on/administrator/keycloak.html).