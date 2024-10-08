# Wazuh LDAP Tests

## Rationale

Create a LDAP User and group Structure, and configure the Wazuh Indexer to test adding multiple users sources to the Wazuh Indexer Authentication and Authorization process.

## Deploy LDAP container

Create an `.env` file, you can use the `.env.example` file provided in the repository

This commands use the password on the `.env.example` file, update it with you ldap admin password

Commands to load LDAP structure

```
docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec openldap ldapadd -x -w "S3cret" -D "cn=admin,dc=wazuh,dc=local" -f /root/01-crate_users_groups.ldif

docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec openldap ldapadd -x -w "S3cret" -D "cn=admin,dc=wazuh,dc=local" -f /root/02-base_users.ldif
  
docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec openldap ldapadd -x -w "S3cret" -D "cn=admin,dc=wazuh,dc=local" -f /root/03-admin_group.ldif

```

Commands to set passwords to users

```
docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec -it openldap ldappasswd -x -D "cn=admin,dc=wazuh,dc=local" -S "uid=user1,ou=users,dc=wazuh,dc=local" -w "S3cret"

docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec -it openldap ldappasswd -x -D "cn=admin,dc=wazuh,dc=local" -S "uid=guest1,ou=users,dc=wazuh,dc=local" -w "S3cret"

docker compose -f ./wazuh-labs/wazuh_ldap/docker-compose.yml exec -it openldap ldappasswd -x -D "cn=admin,dc=wazuh,dc=local" -S "uid=manager1,ou=managers,dc=wazuh,dc=local" -w "S3cret"

```

## Configure Wazuh

Modifications to the `/etc/wazuh-indexer/opensearch-security/config.yml` file in the Authentication section

```
authc:
...
ldap:
        description: "Authenticate via LDAP or Active Directory"
        http_enabled: true
        transport_enabled: true
        order: 1
        http_authenticator:
          type: basic
          challenge: false
        authentication_backend:
          type: ldap
          config:
            enable_ssl: false
            enable_start_tls: false
            enable_ssl_client_auth: false
            verify_hostnames: false
            hosts:
            - 10.1.1.156:389
            bind_dn: "cn=admin,dc=wazuh,dc=local"
            password: "S3cret"
            users:
              primary-userbase:
                base: 'ou=managers,dc=wazuh,dc=local'
                search: '(uid={0})'
              secondary-userbase:
                base: 'ou=users,dc=wazuh,dc=local'
                search: '(uid={0})'
            username_attribute: uid
```

Modifications to the `/etc/wazuh-indexer/opensearch-security/config.yml` file in the Authorization section

```
 authz:
      roles_from_myldap:
        description: "Authorize via LDAP or Active Directory"
        http_enabled: true
        transport_enabled: true
        authorization_backend:
          type: ldap
          config:
            # enable ldaps
            enable_ssl: false
            enable_start_tls: false
            enable_ssl_client_auth: false
            verify_hostnames: false
            hosts:
            - 10.1.1.156:389
            bind_dn: "cn=admin,dc=wazuh,dc=local"
            password: "S3cret"
            rolebase: 'ou=groups,dc=wazuh,dc=local'
            rolesearch: '(member={0})'
            userroleattribute: null
            userrolename: disabled
            rolename: cn
            resolve_nested_roles: true
            users:
              primary-userbase:
                base: 'ou=managers,dc=wazuh,dc=local'
                search: '(uid={0})'
              secondary-userbase:
                base: 'ou=users,dc=wazuh,dc=local'
                search: '(uid={0})'
```

Apply configurations from file `/etc/wazuh-indexer/opensearch-security/config.yml` to the Wazuh Indexer

```
export JAVA_HOME=/usr/share/wazuh-indexer/jdk/ && bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/securityadmin.sh -f /etc/wazuh-indexer/opensearch-security/config.yml -icl -key /etc/wazuh-indexer/certs/admin-key.pem -cert /etc/wazuh-indexer/certs/admin.pem -cacert /etc/wazuh-indexer/certs/root-ca.pem -h 10.1.1.155 -nhnv
```


Apply configurations from file `/etc/wazuh-indexer/opensearch-security/roles_mapping.yml` to the Wazuh Indexer

```
export JAVA_HOME=/usr/share/wazuh-indexer/jdk/ && bash /usr/share/wazuh-indexer/plugins/opensearch-security/tools/securityadmin.sh -f /etc/wazuh-indexer/opensearch-security/roles_mapping.yml -icl -key /etc/wazuh-indexer/certs/admin-key.pem -cert /etc/wazuh-indexer/certs/admin.pem -cacert /etc/wazuh-indexer/certs/root-ca.pem -h 10.1.1.155 -nhnv
```