# Web Scrapper

## Description

This is a web scrapper based on microservices architecture. It is designed to be scalable, fast and work around the clock.

The only reason why I used three different languages is because I wanted to practice them and to get acquainted with their popular frameworks. And, perhaps, ~~to show off~~ to challenge myself.

## Structure:

- **scheduler:** responsible for scheduling the tasks
- **scrapper:** responsible for scrapping the data from websites
- **extractor:** responsible for parsing the data
- **proxy_manager:** responsible for managing the proxies for scrapper
- **db:** responsible for storing the data
