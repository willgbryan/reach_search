# Reach Search App (this setup is pretty broken atm, the streamlit UI is more stable)

## Getting Started

### Setting up Docker

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
2. Create an account during the installation process or via the Docker Hub website.
3. Ensure that Docker Desktop is running on your machine to support the Docker daemon.

### Starting the Application with Docker (WIP)

Currently, (unfortunately) we need 3 separate containers to run this.
Make sure you have Docker desktop running on your machine before executing these commands.

You may need to run the following command in your terminal to run images via the command line:
```bash
docker login
```

### Backend: 

1. Open a terminal.
2. Navigate to the repository's root directory.
3. Run the following command:

```bash
docker build --build-arg OPENAI_API_KEY=<your_api_key> -t backend-service .
```
4. Run the following command:
```bash
docker run --name="backend-service" -p 8000:8000 backend-service
```

### Engine:

1. Navigate to the repository's root directory.
2. Create a new directory to store the engine files.
```bash
mkdir searxng
```
3. Run the following command to start the search engine:
```bash
docker run --network app-network --restart=unless-stopped --name="xng" -d -p 8080:8080 -v "${PWD}/searxng:/etc/searxng" -e "BASE_URL=http://localhost:8080/" -e "INSTANCE_NAME=xng" searxng/searxng
```
4. Run the following command to allow `json` input formats to the engine. This modifies the settings.yml file, adding the `- json` to the formats section.
```bash
sed -i '/formats:/a \ \ - json' searxng\settings.yml
```
5. Restart the `xng` container in the Docker desktop Actions section.

### Frontend:

1. Navigate to the frontend directory from the root of the repository.
```bash
cd frontend
```
2. Run the following command:
```bash
docker build -t frontend .
```
3. Run the following command:
```bash
docker run --name="frontend" -p 3000:3000 frontend
```

# Create a custom network
docker network create app-network

# Run your containers with the `--network` flag
docker run --network app-network --name backend -p 8000:8000 backend-serivce
docker run --network app-network --name frontend -p 3000:3000 frontend