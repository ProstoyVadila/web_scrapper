# Web Scrapper

## Description

This is a web scrapper based on microservices architecture. It is designed to be scalable, fast, manageable via API and work around the clock.

The only reason why I used three different languages is because I wanted to practice them and to get acquainted with their popular frameworks. And, of course, ~~to show off~~ to challenge myself. In real-world projects, I would prefer to use only one.

## Structure:

- **scheduler:** responsible for scheduling the tasks
- **scrapper:** responsible for scrapping the data from websites
- **extractor:** responsible for parsing the data
- **proxy_manager:** responsible for managing the proxies for scrapper
- **db:** responsible for storing the data

### Scheduler

This service is responsible for scheduling the tasks for Scrapper. It is written in Python using FastAPI framework. It sets values to RabbitMQ queue for Scrapper and stores them in Postgres. Scheduler manages routine tasks to refresh the data from the websites as well.

It has a few endpoints which accept a JSON object with the following structure:

POST `/site` - to add a single site to scrapping process and returns the site id

Request:

```json
{
  "url": "https://www.example.com",
  "refresh_interval": "600", // in seconds
  "xpaths": {
    "title": "//title/text()",
    "description": "//meta[@name='description']/@content",
    "keywords": "//meta[@name='keywords']/@content"
  }
}
```

POST `/sites` - to add multiple sites to the queue and returns the list of site ids

Request:

```json
[
    {
        "url": "https://www.example.com",
        "refresh_interval": "600", // in seconds
        "xpaths": {
            "title": "//title/text()",
            "description": "//meta[@name='description']/@content",
            "keywords": "//meta[@name='keywords']/@content"
        }
    },
    ...
]
```

GET `/sites/{id}` - to get the status of the task by id

Request:

```json
{
  "id": "1"
}
```

GET `/expired` - to get the list of sites with expires xpaths

Response:

```json
[
    {
        "id": "1",
        "url": "https://www.example.com",
        "expired_xpaths": {
            "title": "//title/text()",
            "description": "//meta[@name='description']/@content",
            "keywords": "//meta[@name='keywords']/@content"
        }
    },
    ...
]
```

### Scrapper

This service is responsible for scrapping the data from the websites. It is written in Rust using Tokio and Reqwest. It gets the data from RabbitMQ queue and updates it in Postgres.

### Extractor

This service is responsible for parsing the data. It is written in Python. It parses data from websites using xpaths and stores them in db.

### Proxy Manager

This service is responsible for managing the proxies for Scrapper. It is written in Go using Gin framework. It gets the proxies from resource and manages thier availability.
