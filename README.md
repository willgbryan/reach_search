# Reach Search App

## Getting Started

### Setting up Docker

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
2. Create an account during the installation process or via the Docker Hub website.
3. Ensure that Docker Desktop is running on your machine to support the Docker daemon.

### Starting the Application with Docker (WIP)

Currently, (unfortunately) we need 3 separate containers to run this.

Backend: 

1. Open a terminal.
2. Navigate to the repository's root directory.
3. Run the following command:

```bash
docker build --build-arg OPENAI_API_KEY=<your_api_key> -t backend-service .
```

Frontend:

1. Navigate to the frontend directory from the root of the repository.
```bash
cd frontend
```
2. Run the following command:
```bash
docker build -t frontend .
```

Engine:

1. Navigate to the repository's root directory.
2. Create a new directory to store the engine files.
```bash
mkdir searxng
```
3. Run the following command to allow `json` input formats to the engine. This modifies the settings.yml file, adding the `- json` to the formats section.
```bash
sed -i '/formats:/a \ \ - json' searxng\settings.yml
```
4. Run the following command to start the search engine:
```bash
docker run --restart=unless-stopped --name="xng" -d -p 8080:8080 -v "${PWD}/searxng:/etc/searxng" -e "BASE_URL=http://localhost:8080/" -e "INSTANCE_NAME=xng" searxng/searxng
```

Make sure you have Docker running on your machine before executing these commands.
