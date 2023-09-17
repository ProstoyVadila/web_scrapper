# RabbitMQ Configuration

## User Management

To create users and set permissions, you need to add them to the [definitions.sjon](conf/definitions.json) file.

and update [init.sh](scripts/init.sh) and [Dockerfile](Dockerfile) files with the new users.

## TODO:

- [ ] figure out how to configure users and permissions from the rabbitmq container

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

```json
    "exchange": [
      {
        "name": "urls_to_crawl_exchange",
        "vhost": "/",
        "type": "direct",
        "durable": true,
        "auto_delete": false,
        "internal": false,
        "arguments": {}
      },
      {
        "name": "html_to_parse_exchange",
        "vhost": "/",
        "type": "direct",
        "durable": true,
        "auto_delete": false,
        "internal": false,
        "arguments": {}
      }
    ],
    "queues": [
      {
        "name": "urls_to_crawl_queue",
        "vhost": "/",
        "durable": true,
        "auto_delete": false,
        "arguments": {}
      },
      {
        "name": "html_to_parse_queue",
        "vhost": "/",
        "durable": true,
        "auto_delete": false,
        "arguments": {}
      }
    ]
```
