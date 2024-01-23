# Reach Search App

## Getting Started

### Setting up Docker

1. Download and install Docker Desktop from the [official website](https://www.docker.com/products/docker-desktop).
2. Create an account during the installation process or via the Docker Hub website.
3. Ensure that Docker Desktop is running on your machine to support the Docker daemon.

### Configuring Environment Variables

Before starting the application, you need to set up the necessary environment variables:

1. `OPENAI_API_KEY`: This is your OpenAI API key used for making API requests.
2. `SEARX_HOST`: This should be set to the URL of your Searx instance, which is "http://localhost:8080" by default.

To set these environment variables:

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

### Starting the SearXNG Engine Container

To use the SearXNG search engine with the application, you need to run it in a Docker container. Follow these steps to set up and start the SearXNG engine:

1. Create a new directory for the SearXNG engine. It is recommended to create this directory outside of your application's directory to keep things organized:

```bash
mkdir SearXNG
cd SearXNG
```

2. Run the following command to start the SearXNG container:

```bash
docker run --restart=unless-stopped --name="xng" -d -p 8080:8080 -v "${PWD}/searxng:/etc/searxng" -e "BASE_URL=http://localhost:8080/" -e "INSTANCE_NAME=xng" searxng/searxng
```

This command will:

- Start a new Docker container named `xng`.
- Restart the container unless it is explicitly stopped.
- Bind the container's port `8080` to port `8080` on the host machine.
- Create a volume that maps the `searxng` directory in the current working directory to `/etc/searxng` inside the container.
- Set environment variables for `BASE_URL and INSTANCE_NAME`.

After running this command, the SearXNG engine should be accessible at `http://localhost:8080/`. Make sure this URL matches the `SEARX_HOST` environment variable set in the application configuration.

### Starting the Application

#### Backend Setup

1. Navigate to the repository's root directory.
2. Activate your virtual environment:
   - On Windows: `.\venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
3. Install the required packages from `requirements.txt`:
4. Navigate to the `reach_search/backend` directory.
5. Start the backend service:

#### Frontend Setup

1. Open a new terminal.
2. Navigate to the `reach_search/frontend/reach-search-app` directory.
3. Install the necessary npm packages (if you haven't already):
4. Start the frontend service with `npm start`: