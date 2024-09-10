import json
import random
import requests
import os
import time

def load_logs(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def post_log(log):
    headers = {
        'Content-Type': 'application/json',
        'DD-API-KEY': os.environ['DD_API_KEY']
    }

    url = 'https://http-intake.logs.datadoghq.com/v1/input'

    response = requests.post(url, json=log, headers=headers)
    return response.status_code, response.text

def log_message(message, log_mode):
    if log_mode == "stdout":
        print(message)
    elif log_mode == "file":
        with open("/app/logalanche.log", "a") as log_file:
            log_file.write(f"{message}\n")
    # If log_mode is 'none', do nothing (no logging)

def main():
    frequency_seconds =  int(os.getenv('FREQ_SECONDS', 5))
    log_mode = os.getenv('LOG_MODE', 'stdout')  # Options: 'stdout', 'none', 'file'

    logs = load_logs('logs.json')

    while True:
    
        log = random.choice(logs)
        status_code, response_text = post_log(log)

        log_message(f"POST {status_code}: {response_text}", log_mode)

        time.sleep(frequency_seconds)

if __name__ == '__main__':
    main()

