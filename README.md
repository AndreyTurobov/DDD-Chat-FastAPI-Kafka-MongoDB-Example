# DDD Chat (FastAPI, Kafka, MongoDB) Application Example

This is the basic sample for FastAPI application configured to use Docker Compose, Makefile, and MongoDB. This application is based on modern Domain Driven Development architecture.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [MongoDB](https://www.mongodb.com/docs/drivers/python-drivers/)
- [Mongo-Express](https://github.com/mongo-express/mongo-express)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. Install all required packages in `Requirements` section.


### Implemented Commands

* `make app` - up application 
* `make app-logs` - follow the logs in app container
* `make app-down` - down application
* `make app-shell` - go to containerized interactive shell (bash)
* `make storages` - up database/infrastructure
* `make storages-down` - down database/infrastructure
* `make all` - up both application and database/infrastructure 
* `make clean` - down both application and database/infrastructure

### Most Used Specific Commands

* `make test` - test application with pytest