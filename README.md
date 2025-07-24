# ADR Dataset Uploader

This project is a simple tool to upload an Architecture Decision Record (ADR) dataset from a JSONL file to a MongoDB collection. It uses Docker and Docker Compose to streamline the setup and execution process.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuration

Follow the steps below to set up the project.

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:samuelcluna/adr-dataset-builder.git
    cd adr-dataset-builder
    ```

2.  **Create the environment file:**
    Copy the example `.env_sample` file to a new file named `.env`. This file will be used by Docker Compose to configure the container's environment.
    ```bash
    cp .env_sample .env
    ```

3.  **Configure environment variables:**
    Open the `.env` file and replace the placeholder values with your actual MongoDB credentials and settings.


4.  **Prepare your data:**
    Create a file named `data.jsonl` in the extraction directory root. Add the documents you want to upload, with one JSON object per line. The `docker-compose.yml` is configured to mount this file inside the container.

## How to Run

With Docker and Docker Compose installed and the environment configured, run the following command in the project root:

```bash
docker-compose up
```

This command will:
1.  Build the Docker image as defined in the `Dockerfile`.
2.  Create and start a container for the `adr-uploader` service.
3.  The `app/main.py` script inside the container will execute, reading `data.jsonl` and inserting the documents into your MongoDB collection.
4.  You will see a message in the console indicating how many documents were inserted successfully.

If you need to rebuild the image after making changes to the `Dockerfile` or `requirements.txt`, use the `--build` flag:
```bash
docker-compose up --build
```
