# Reach Search App

## Getting Started

### Setting up Docker

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
2. Create an account during the installation process or via the Docker Hub website.
3. Ensure that Docker Desktop is running on your machine to support the Docker daemon.

### Configuring Environment Variables

Before starting the application, you need to set up the necessary environment variables:

1. Open the backend.env file and update the following.
2. `OPENAI_API_KEY`: This is your OpenAI API key used for making API requests.
3. `SEARX_HOST`: This should be set to the URL of your Searx instance, which is "http://localhost:8080" by default.

You can also set these environment variables via the command line:

- On Windows:
```bash
set OPENAI_API_KEY=your_openai_api_key_here
set SEARX_HOST=http://localhost:8080
```

- On macOS/Linux:
```bash
export OPENAI_API_KEY=your_openai_api_key_here
export SEARX_HOST=http://localhost:8080
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.


### Starting the Application with Makefile (WIP)

Instead of starting each component separately, you can use the provided Makefile to build and run the backend, frontend, and SearXNG engine. Follow these steps:

1. Open a terminal.
2. Navigate to the repository's root directory.
3. Run the following command to build and start all components:

```bash
make all
```

This will execute the following:

- Build the Docker image for the backend service.
- Build the Docker image for the frontend application.
- Run the backend service in a Docker container.
- Run the frontend application in a Docker container.
- Set up and run the SearXNG engine in a Docker container.

To stop all running containers, you can use:

```bash
make stop
```

To remove all containers, use:

```bash
make clean
```

To remove all Docker images, use:

```bash
make clean-images
```

Make sure you have Docker running on your machine before executing these commands.
