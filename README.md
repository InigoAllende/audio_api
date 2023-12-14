# audio_api
This service provides several endpoints that allow to manage audio files. 

The application stores the files using cryptography to encrypt the files that are stored on the server side.

To be able to send requests to the application and api key is required.

The encryption and api keys are fetched from the environment. The project is set with some default values to make running it easier but new keys should be generated in a production environment.

API documentation can be accessed once the application is running under `/docs` or `/redoc` depending on the preferred format.

### Pre-requisites
Please be sure to have the following requirements installed:

* This project uses [`poetry`](https://python-poetry.org/) for dependency management
* [`direnv`](https://direnv.net/) is optional but it might make life easier to handle the project environment variables. An `.env.example` is provided in the project for reference. Rename the file to `.env` and update the environment variables as needed.
* [`docker`](https://docs.docker.com/engine/install/) and [`docker compose`](https://docs.docker.com/compose/install/) are used to containerize the application

## Run locally
To run the project in your machine please follow these steps
* `poetry install` will install the project dependencies, using a virtual environment is encouraged.
* `make run-local` will start a uvicorn web server in your machine
* Same for the tests, they can be run using the makefile script `make tests`

## Run with docker
The docker image can be built and tagged by executing the command `make build`. By default this will build an image with the tag `latest` it is possible to pass a `version` parameter to build a specific one (`make build version=0.0.1`). This image can then be pushed to a docker registry of choice.

To run an instance of the application in docker execute the command `make run`. This will use docker compose to build and start a container with the service.

The dockerized version of the application mounts the folder `./audio_file_storage` that is present in the project folder as a volume and will use this to store the uploaded files.


## Afterthoughts
- Right now the application uses a volume in the machine running. If it is used in conjuction with some cloud service, this would need to be updated to work with some bucket instead.
- I did not add logic on the upload endpoint to handle cases of uploading files with conflicting names. Moving forward, this and an endpoint to delete files would be necessary.
- If a more scalable application is needed a rework of how the files are stored and the endpoints might be necessary. For example store files in subfolders based on specific api keys, which would allow to have user or application groups with different keys and avoid users overwritten each other's files due to name conflicts.
- I considered adding a database to manage some information about the files. But conisered it was a bit too much for the current scale of the project, since there was no need to store user credentials and all of the necessary data that is required by the specification is contained within the files themselves.
- I was a bit confused about decibels full scale. I was not sure whether the endpoint would take a value in decibels or the increase of decibels in dBFS. I went with the simplest approach, designing an API that takes the increase in decibels but this should be relatively easy to modify if a different formula is needeed.
