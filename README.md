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