# wazuh-labs
Wazuh labs and tests

Create and `.env` file, you can use the `.env.example` file provided in the repository

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
