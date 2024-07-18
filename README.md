# Chat Backend Performance Test

This project compares the performance of chat backend implementations in Node.js, Rust, and Go.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

- `node/`: Node.js backend implementation
- `rust/`: Rust backend implementation
- `go/`: Go backend implementation
- `tests/`: Test scripts and configurations
- `database/`: Database initialization scripts
- `docker-compose.yml`: Defines our multi-container Docker application
- `results/`: Directory where test results will be stored

## Quick Start

1. Clone the repository:

```
git clone https://github.com/your-username/chat-backend-performance-test.git
cd chat-backend-performance-test
```

2. Build the Docker images:

```
docker compose build
```

3. Start the services:

```
docker compose up -d
```

4. Run the performance tests:

```
docker compose run test-runner
```

5. Clean up:
```
docker compose down
```
