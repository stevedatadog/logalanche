# logalanche

logalanche is a simple application that simulates log generation for
observability demonstrations and teaching environments. It reads predefined log
entries from a JSON file, picks a random log entry, and sends it to an external
REST API.

## Features

- Reads logs from a JSON file (can be user-provided or defaults to a built-in
  file).
- Sends logs to an external REST API (e.g., Datadog Logs).
- Configurable logging behavior for logalanche itself (log to STDOUT, disable
  logging, or log to a file).

## Requirements

- Docker
- Datadog API Key

## Usage

### 1. Building the Docker Image

To build the Docker image, run:

```bash
docker build -t logalanche:latest .
```

### 2. Running the Docker Container

#### Default Usage

By default, logalanche reads from a built-in `logs.json` file and sends log
entries to the Datadog API. To run the container, use:

```bash
docker run \
  -e DD_API_KEY="your-api-key-here" \
  logalanche
```

#### Using a Custom Log File

You can mount your own logs.json file to the container. For example:

```bash
docker run \
  -v /path/to/your/logs.json:/app/logs.json \
  -e DD_API_KEY="your-api-key-here" \
  logalanche
```

#### Logging Modes

logalanche supports three logging modes for its own logging:

1. stdout (default): Logs messages to STDOUT.
2. none: Disables logging.
3. file: Logs messages to a file inside the container (`/app/logalanche.log`).

You can control the logging behavior by setting the LOG_MODE environment
variable.

- **Log to STDOUT (default):**

```bash
docker run \
  -e DD_API_KEY="your-api-key-here" \
  logalanche
```

- **Disable Logging:**

```bash
docker run \
  -e DD_API_KEY="your-api-key-here" \
  -e LOG_MODE="none" \
  logalanche
```

- **Log to a File:**

```bash
docker run \
  -e DD_API_KEY="your-api-key-here" \
  -e LOG_MODE="file" \
  logalanche
```

The logs will be written to `/app/logalanche.log` inside the container. To access
the log file, you can mount a directory from the host:

```bash
docker run \
  -v /path/to/logdir:/app \
  -e DD_API_KEY="your-api-key-here" \
  -e LOG_MODE="file" \
  logalanche
```

## JSON File Format

The JSON file should be an array of items. Beyond that, it's up to you. The
example logs.json contains an array of objects, with each object containing the
following fields:

- timestamp: A UTC timestamp in ISO 8601 format.
- status: The log level or status (e.g., INFO, ERROR).
- message: A text message describing the log event.

Example logs.json format:

```json
[
  {
    "timestamp": "2024-09-10T17:43:37Z",
    "status": "INFO",
    "message": "All dependencies up to date"
  },
  {
    "timestamp": "2024-09-10T18:00:00Z",
    "status": "ERROR",
    "message": "Error detected in module XYZ"
  }
]
```

## License

This project is licensed under the MIT License.
