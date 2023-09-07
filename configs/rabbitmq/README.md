# RabbitMQ Configuration

## User Management

To create users and set permissions, you need to add them to the [definitions.sjon](conf/definitions.json) file.

and update [init.sh](scripts/init.sh) and [Dockerfile](Dockerfile) files with the new users.

```json
  "users": [
    {
      "name": "admin",
      "password_hash": "<admin_hashed_password>",
      "hashing_algorithm": "rabbit_password_hashing_sha256",
      "tags": "administrator"
    },
    {
      "name": "guest",
      "password_hash": "<guest_hashed_password>",
      "hashing_algorithm": "rabbit_password_hashing_sha256",
      "tags": ""
    }
  ],
  "permissions": [
    {
      "user": "admin",
      "vhost": "/",
      "configure": ".*",
      "write": ".*",
      "read": ".*"
    }
  ],
```

## Create queues

To create queues, you need to add them to the [definitions.sjon](conf/definitions.json) file.

```json
"queues": [
    {
    "name": "queue1",
    "vhost": "/",
    "durable": true,
    "auto_delete": false,
    "arguments": {}
    }
],
```

## Manual user creation

For a manual user creation.
Generate a password's hash for the rabbitmq management user:

```bash
    python3 scripts/generate_pass.py <username>
```

Add password's hash and username to the [definitions.sjon](conf/definitions.json) file.
