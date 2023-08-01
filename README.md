# RideAPI [![Python application](https://github.com/SWoto/RideAPI/actions/workflows/python-app.yml/badge.svg)](https://github.com/SWoto/RideAPI/actions/workflows/python-app.yml)
The goal is to create an API that use microservices and message brokers to comunicate between them.

# Project Description
An API that handles rides. It will have:
- Users
    - Driver
    - Passenger 
- Vehicles 
- Rides

This will be distributed within three services:
- Users
- Requests, for the rides
- Vehicles

## Users
Users API will handle subscription and have two options, driver and passenger. This will also handle authentication to request/receive rides.

## Vehicles
This will have the registered vehicles and its consuption (km/L) that is going to be used to calculate the rate. Each vehicle must be owned by one driver.

## Requests
Requests will connect passengers and drivers. Saving the distancy and informing the user the total amount.

# How to use it
## Docker
This code uses postgres, [pgadmin](http://localhost:15433) and redis. All three of them can be set and run with the compose.yml file and two commands in the terminals.
```powershell
docker compose create
docker compose up
```

In case of wanting to rebuild it all and get it running:
```powershell
 docker compose up -d --build  
```

**Note**: It depends on the .env file and some of its parameters.
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- POSTGRES_DB=
- PGADMIN_DEFAULT_EMAIL=
- PGADMIN_DEFAULT_PASSWORD=

If you've just cloned the repository, there will be no .env file, though note that there is a .env.example. Use it as a basis to set-up your configuraiton.

## pgAdmin
On the first run, to set up pgadmin, you'll need the parameters mentioned just before and also the container ip-address.

```powershell
docker container ls
docker inspect <postgres_CONTAINER_ID>
```

This will present its network settings and, in it, it's ip.

Another option, as easier, is to user the postgres service name, same used in the docker-compose file.

## Migrate (Alembic)
Always set the enviroment variable to use all the blueprints. **Remember to remove it latter.**
```powershell
$env:ALEMBIC_MIGRATE="1"
```

On the first run, use 
```powershell
flask --app base_app db init
```

To update the db with new changes:
```
flask --app base_app db migrate -m "<some text>"
```
:exclamation: **ALWAYS CHECK THE GENERATED FILES, it might cause unwanted effects when upgrading or downgrading**
```
flask --app base_app db upgrade
```

### Disclaimer
Given that the database is running locally and not in a server, everytime that this program is built in a new computer, 
the database must be initiated again. Due to this, the ´src/database/migrations/versions´ will be added to the .gitignore file.

## Unittest
```
python -m unittest discover -v -s tests -p "test_*.py"
```
