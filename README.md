# Django / docker x docker-compose / graphql - experiment

## Prerequisites

1. Must have [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed.

## Pre-setup

1. Change/duplicate `.env.tpl` to `.env` and edit the values inside accordingly

------------------------------

## 1. For building local development
`make local`

## To stop and remove the dockerize environment
`make down`

## To makemigrations
`make migrations name=` then the name you want to commit

# How to

## After building your local development you must create a superuser account
`http://localhost:8000/api/admin/graphiql` <br />
i invole [Mutations](https://docs.graphene-python.org/projects/django/en/latest/mutations/) from [Graphene Django](https://docs.graphene-python.org/projects/django/en/latest/)<br />
`mutation {
  register(
    email: "kentoyfueconcillo@gmail.com",
    username: "admin",
    password1: "Pasmo.123",
    password2: "Pasmo.123",
    first_name: "kent",
    last_name: "dddd"
  ) {
    success,
    errors,
    # token
  }
}
`

## Then login in django admin
[http://localhost:8000/admin](http://localhost:8000/admin)

## To test a graphql by graphqil interface navigate to 
[http://localhost:8000/api/admin/graphiql](http://localhost:8000/api/admin/graphiql)

## Use pg admin
1. Navigate to <IP>:5050
2. Use this ff credentials
   - Email: kentoyfueconcillo@gmail.com
   - Password: ismellsomethingfishy
3. Click add server 
   - General > Name: put name you want
   - Connection
     - Hostname: db
     - Port: 5432
     - maintenance db: postgres
     - username: postgres
     - password: ismellsomethingfishy
 4. The database will be created
 5. Navigate to this path.
     - your name inputed > databases > postgres > schemas > tables
     
## Query in a single pythone file
`make test-queries`

## Do fake migration
`make fakemigration application=<your app>`

# EXTRAS
## To run a editor inside docker container using bpython
`make editor`

# FEATURES!!

### [Docker](https://docs.docker.com/compose/) <br />
deployment of applications inside software containers

### [Django Rest Framework](https://www.django-rest-framework.org/) <br />
Browsable api

### [PipEnv](https://pipenv.readthedocs.io/) <br />
For installing dependencies

### [Nginx](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) <br />
As proxy

### [Daphne](https://github.com/django/daphne) <br />
As the interface server

### [Channels](https://channels.readthedocs.io/en/latest/)
Handling connections and sockets asynchronously

### [Redis](http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html) <br />
As the backend

### [Annoying](https://github.com/skorokithakis/django-annoying) <br />
This django application eliminates certain annoyances in the Django framework.

### [Django Graphql Auth](https://github.com/PedroBern/django-graphql-auth) <br />
Abstract all the basic logic of handling user accounts out of your app, so you don't need to think about it and can get up and running faster.

No lock-in. When you are ready to implement your own code or this package is not up to your expectations , it's easy to extend or switch to your implementation.

### [Graphql-Python/Graphene-Django](http://docs.graphene-python.org/projects/django/en/latest/) <br />
Primary focus here is to give a good understanding of how to connect models from Django ORM to graphene object types.

### [PG Admin 4](https://www.pgadmin.org/) <br />
The pgAdmin documentation for the current development code, and recent major releases of the application is available for online browsing. Please select the documentation version you would like to view from the options below.

### FAQ
* TypeError: 'module' object is not callable
This is cause by django 3.7 and pipenv 18.1 version. So to fix this 

	- `pip install pipenv`
	- `pipenv run pip install pip==18.0`
	- `pipenv install`
    
    or just type
    
    - `make fix`
    
* I'm getting `ERROR: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io ... : read: connection refused` error.

    * Do `docker-machine ssh default`, then edit the resolve file `sudo vi /etc/resolv.conf` change the nameserver value to `1.1.1.1` or `8.8.8.8`
    
* Bind for `0.0.0.0:5432` failed: port is already allocated
    
    * `docker ps`
    * after that this will showen up <br />
    ```13b484047582        postgres:9.6.5-alpine   "docker-entrypoint.s…"   28 hours ago        Up 5 hours          0.0.0.0:5432->5432/tcp   sample_db```
    
    * the conflict is ```0.0.0.0:5432->5432/tcp```
    * we need to stop the docker container first
    * `$ docker stop 13b484047582`
    * then remove 
    * `$ docker remove 13b484047582`
    * then re run the environment
    * `$ make local(rebuilding container) / make up(starting container)`

    
    
