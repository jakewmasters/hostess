# hostess
A webserver + templating engine combo written in pure Python. 

## What is it?
A webserver written in pure Python bundled with a simple template rendering engine. 

The webserver just uses `socket` and the template rendering engine is inspired by Django's templating engine. 

## Why did I write it?
I wrote this because I strongly dislike using gigantic pieces of software whose codebase I don't understand when I can make something simple instead. 

![relevant meme I made](webserver-meme.PNG)

This project is based off of a variation I wrote for an industry project. That version made use of REST API calls to provide data and was served from a Docker container. 

Rather than taking the time to learn how to configure Nginx to work for the specific use case I needed it to work for, I decided to learn more about HTTP and write my own solution. 

This repository reflects a fairly minimal working solution. Adding additional modular features is easy: just add new routes, handlers, and `data_library()` logic. 

## How does it work?
1. The webserver listens on a network port for HTTP requests. 
2. Upon receiving a request, the webserver determines whether a URL path or a specific file is being requested. 
    - If a specific file is being requested, a handler for that file type is called. 
    - If a URL path is being requested, the webserver calls the handler for the corresponding HTML file. 
3. The handler is then responsible for sending back a response. 
    - This might just be a static file like an image. 
4. If the response involves an HTML file, the handler looks up the correct HTML template and passes it to the template renderer. 
5. The template renderer parses the file for special tokens. 
6. Based on code added to the `data_library()` function and the cookies contained in the request's HTTP headers, new values are rendered into the HTML templates. 
7. Finally, the HTML handler sends back the rendered template. 

I don't do a ton of error checking, just enough to make it usable. 

## How do I run it?
If you want to run this on your local machine, just run: 
```
$ python src/webserver.py
```

If you want to run this in a "production" way (whatever that actually means), I've had success doing the following: 
1. Find a Linux server. 
2. Clone this repository to `/srv/test`. 
3. Create a Dockerfile that looks kinda like this: 
```
FROM [some Docker image with Python and pip]

WORKDIR /srv/test

COPY . /srv/test

EXPOSE 8000

CMD ["python", "src/webserver.py"]
```
4. Build a Docker image: `docker build --tag=testimage .`
5. Run your new Docker image: `docker run -d -p 80:8000 testimage`
6. See if you can browse to the pages you're expecting to be served. 

Some variation of this should work. 
