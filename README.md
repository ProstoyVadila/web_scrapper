# Web Scrapper

## Description

This is a web scrapper based on microservices architecture. It is designed to be scalable, fast, manageable via API and work around the clock. The main idea behind this scrapper is to get a lot of persistent data from websites on a daily basis. It's not suitable for one-time scrapping.

### Why microservices?

I chose microservices architecture because it's scalable. It's easy to add new services and scale them independently. For example, if we need to crawl sites faster, we can just add more Scrapper instances. If we need to add new functionality, we can just add new services (for example, services to transform and load data to get a whole ETL process).

### Why Python, Rust and Go?

The only reason why I used three different languages in this project is because I wanted to practice them and to get acquainted with their popular frameworks. And, of course, ~~to show off~~ to challenge myself. In real-world projects, I would definitely prefer to use only one.

The main idea is to use a language that is suitable for the task. For example, I used Python for Scheduler because it's easy to write and it's not the most performance-critical part of the project. I used Rust for Scrapper because it's fast and works fine under high load (this service's performance is the most crucial). I used Go for Proxy Manager because it's fast and easy to write and maintain.

## Structure:

![Structure](/configs/Untitled-2023-09-04-1617.png)

- **api_backend:** responsible for adding new sites to scrapping process and getting the status of the task
- **scheduler:** responsible for scheduling the tasks
- **scrapper:** responsible for scrapping the data from websites
- **extractor:** responsible for parsing the data
- **proxy_manager:** responsible for managing the proxies for scrapper
- **db:** responsible for storing the parsed data
- **rabbitmq:** responsible for communication between services

### Scheduler

This service is responsible for scheduling the tasks for Scrapper. It is written in Python using FastAPI framework. It sets values to RabbitMQ queue for Scrapper and stores them in Postgres. Scheduler manages routine tasks to refresh the data from the websites as well.

### Scrapper

This service is responsible for scrapping the data from the websites. It is written in Rust using Tokio and Reqwest. It gets the data from RabbitMQ queue and updates it in Postgres.

### Extractor

This service is responsible for parsing the data. It is written in Python. It parses data from websites using xpaths and stores them in db.

### Proxy Manager

This service is responsible for managing the proxies for Scrapper. It is written in Go using Gin framework. It gets the proxies from resource and manages thier availability.

### Database

figure out what to use (postgres, mongo, scylladb)
