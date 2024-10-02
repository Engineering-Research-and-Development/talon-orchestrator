# Talon Python API

This repository contains the backend API for the Talon application, developed using Python 3.10.6 or later

## Description

This is a simple Python Flask application that demonstrates how to integrate TensorFlow into a web application. The application uses Flask to create a web server and TensorFlow for machine learning tasks.

--- 

<br>

### Prerequisites

Before running the application, make sure you have the following dependencies installed:

- Python 3.x
- Flask
- TensorFlow
- Docker (for Dockerized deployment)

<br>

### Clone

Clone the repository:

   ```bash
   git clone https://gitlab.ubitech.eu/pdml/talon/talon-python.git
   ```

Navigate to the project directory:

   ```bash
   cd talon-python
   ```

Install the required Python packages using a virtual environment:

   ```bash
   # Virtualenv modules installation (Unix based systems)
   virtualenv env
   source env/bin/activate
   
   # Virtualenv modules installation (Windows based systems)
   # virtualenv env
   # .\env\Scripts\activate
   pip install -r requirements.txt
   ```

<br>

### Local Deployment

To deploy the application locally, follow these steps:

1. Setup the Flask environment:

   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   // OR 
   (Windows CMD) set FLASK_APP=run.py
   (Windows CMD) set FLASK_ENV=development
   // OR
   (Powershell) $env:FLASK_APP = ".\run.py"
   (Powershell) $env:FLASK_ENV = "development"
   ```

2. Start the Flask API server:

   ```bash
   flask run
   ```

> The API will be accessible at  `http://localhost:5000`. Use the API via `POSTMAN` or `Swagger Dashboard` at `localhost:5000`.

<br>

### Dockerized Deployment

To deploy the application using Docker, follow these steps:

1. Build the Docker image:

   ```bash
   docker build -t talon-python .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 5000:5000 talon-python
   ```

> The API will be accessible at `http://localhost:5000`.

<br>

### Docker-compose Deployment

To deploy the application using Docker-compose, follow these steps:

1. Build the application:

   ```bash
   mvn clean package
   ```

2. Run the Docker container:

   ```bash
   docker-compose up -d
   ```

> The API will be accessible at `http://localhost:5000`.

<br>


### Test

To run tests:

```bash
   #for pytest
   flask tests

   #for unittest
   flask unittests

```

### API Documentation

The API documentation can be accessed through the following endpoint: `http://localhost:5000/swagger/`

<br>

### Configuration

The application can be configured using the following environment variables:

- `HOST_PORT`: The exposed Port number of the application when deployed with docker/docker-compose
- `PORT`: Port number of the application

Ensure that these environment variables are properly set before running the application.

> You can modify the Flask application's behavior by editing the config.py file.