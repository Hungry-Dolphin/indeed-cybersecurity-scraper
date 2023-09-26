# indeed-cybersecurity-scraper 

This is a project where I (hopefully) create a dockerised web application to manage what certifications are asked for in cybersecurity jobs

# Usage
In my case I run it on port 5001 because 5000 was already taken. 
```
docker build --tag flask-scraper-app . 
docker run -d -p 5001:5000 flask-scraper-app 
```

# Modules
## Selenium
Lets start with the biggest part of this project. Indeed does have an API but they want you to jump though some hoops.

Hoops which I am not willing to jump though. Because of this we will use the Selenium webdriver to automatically scrape the Indeed website. 
Indeed does not like bots and uses cloudflare to swat them down. In daily usage you should not notice this. Since this application spoofs everything to make it look like a legit request.
Not like the 1 request per day I plan on sending out should matter much for a site like Indeed. 

Please note this application does NOT!!! spoof your IP. Use it with caution. Most free VPN's will make you pass a cloudflare bot test. The easiest way to avoid this is using an IP which is not detected as a VPN. How you go about this is up to you.

## Docker
Because we have to install our own webdriver binaries to succesfully use Selenium we cant use a light flask python Docker image. This project just uses an Ubuntu image because it just works. 

## Flask
Because I don't feel like having to drop into a Docker shell every time I want to see data this application runs a Flask webserver to display data.




# TODO
- ~~Set up flask webserver to serve me a webserver on some port~~
- Write a function (most likely using selenium since indeed uses js to serve content) to scrape job postings
- Do some analysis on these job postings to see what certifications they ask for 
- ~~Dockerise this application so I can run this on my home server without hassle~~


# TODO's later
- Don't just copy the entire workdir in the dockerfile
- Find a less bloated Docker image to use