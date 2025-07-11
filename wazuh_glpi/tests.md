# Command used

Authentication with user-token

```
curl -X GET -H 'Content-Type: application/json' -H "Authorization: user_token <USER_TOKEN>" -H "App-Token: <APP_TOKEN>" 'http://glpi00.wazuh.local/apirest.php/initSession?get_full_session=true'
```

# Session handling

This approach uses `jq` that might not be available in a minimal OS installation

```
SESSION_TOKEN=$(curl -X GET -H 'Content-Type: application/json' -H "Authorization: user_token <USER_TOKEN>" -H "App-Token: <APP_TOKEN>" 'http://glpi00.wazuh.local/apirest.php/initSession'| jq -r '.["session_token"]')

curl -X POST -H 'Content-Type: application/json' -H "Session-Token: $SESSION_TOKEN" -H "App-Token: <APP_TOKEN>" -d '{"input": {"name": "Ticket test #1", "content": "This is the Ticket Test #1 description"}}' 'http://glpi00.wazuh.local/apirest.php/Ticket/'
```
