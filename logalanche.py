import json
import random
import requests
import os
import time
import sys

def load_logs(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        log_message(f"Error: {file_path} not found.")
        return []
    except json.JSONDecodeError:
        log_message(f"Error: Failed to parse {file_path}. Make sure it is valid JSON.")
        sys.exit(1)
        exit

def post_log(log):
    headers = {
        'Content-Type': 'application/json',
        'DD-API-KEY': os.environ['DD_API_KEY']
    }

    url = 'https://http-intake.logs.datadoghq.com/v1/input'

    response = requests.post(url, json=log, headers=headers)
    return response.status_code, response.text

def log_message(message):

    # Set the logging mode, default to 'stdout'
    log_mode = os.getenv('LOG_MODE', 'stdout')  # Options: 'stdout', 'none', 'file'

    if log_mode == "stdout":
        print(message)
    elif log_mode == "file":
        with open("/app/logalanche.log", "a") as log_file:
            log_file.write(f"{message}\n")
    # If log_mode is 'none', do nothing (no logging)

def main():
    # Set frequency_seconds, default to 5 if FREQ_SECONDS is not set
    frequency_seconds = int(os.getenv('FREQ_SECONDS', 5))
    
    # Load log entries from logs.json
    logs = load_logs('logs.json')

    if not logs:
        log_message(f"No logs to process. Exiting.")
        return

    while True:
        log = random.choice(logs)
        status_code, response_text = post_log(log)

        log_message(f"POST {status_code}: {response_text}")

        # Sleep for the configured interval before sending the next log
        time.sleep(frequency_seconds)

if __name__ == '__main__':
    main()

