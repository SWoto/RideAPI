# RideAPI
The goal is to create an API that use microservices and message brokes to comunicate between them.

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
Requests will connect users and drivers. Saving the distancy and informing the user the total amount while handling the payment.

# How to use it
## Docker
This code uses postgres, [pgadmin](http://localhost:15433) and redis. All three of them can be set and run with the compose.yml file and two commands in the terminals.
```powershell
docker compose -f .\docker-compose.yml create
docker compose up
```

**Note**: It depends on the .env file and some of its parameters.
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- POSTGRES_DB=
- PGADMIN_DEFAULT_EMAIL=
- PGADMIN_DEFAULT_PASSWORD=

## pgAdmin
On the first run, to set up pgadmin, you'll need the parameters mentioned just before and also the container ip-address.

```powershell
docker container ls
docker inspect <postgres_CONTAINER_ID>
```

This will present its network settings and, in it, it's ip.