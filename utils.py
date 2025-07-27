## Logging ##
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
RESET = '\033[0m'

import json
import csv
import os
from datetime import datetime

LOG_FILE = "llm_call_log.jsonl"

def log_success_to_file(my_base_url, user_query, my_model, my_model_response, start_time, end_time, token_usage=None):
    log_entry = {
        "timestamp": datetime.fromtimestamp(start_time).isoformat(),
        "duration_seconds": round(end_time - start_time, 2),
        "model": my_model,
        "endpoint": my_base_url,
        "prompt": user_query,
        "response": my_model_response,
        "token_usage": token_usage
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def log_success_plain(my_base_url, user_query, my_model, my_model_response, token_usage=None):
    print(f"{GREEN}|--------------------------------------{RESET}")
    print(f"{GREEN}| Successful Call {RESET}to model: {MAGENTA}{my_model}{RESET} @ {CYAN}{my_base_url}{RESET}")
    print(f"{GREEN}| {RESET}With query: {YELLOW}{user_query}{RESET}")
    print(f"{GREEN}| {RESET}and model response: {MAGENTA}{my_model_response}{RESET}")
    if token_usage:
        print(f"{GREEN}| {RESET}Token usage: {CYAN}{token_usage}{RESET}")
    print(f"{GREEN}| --------------------------------------{RESET}")

def log_error_plain(my_base_url, user_query, my_model, status_code, error_text):
    print(f"{RED}Error during call to: {CYAN}{my_base_url}{RESET}")
    print(f"Prompt: {YELLOW}{user_query}{RESET}")
    print(f"Model: {MAGENTA}{my_model}{RESET}")
    print(f"{RED}Status Code: {status_code}{RESET}")
    print(f"{RED}Error Message: {error_text}{RESET}")

def convert_jsonl_to_csv(jsonl_file=LOG_FILE, csv_file="llm_call_log.csv"):
    if not os.path.exists(jsonl_file):
        print(f"{RED}No log file found at {jsonl_file}{RESET}")
        return

    with open(jsonl_file, "r", encoding="utf-8") as jf, open(csv_file, "w", newline='', encoding="utf-8") as cf:
        writer = None
        for line in jf:
            data = json.loads(line)
            # Flatten token usage if exists
            if isinstance(data.get("token_usage"), dict):
                for k, v in data["token_usage"].items():
                    data[f"token_usage_{k}"] = v
                del data["token_usage"]

            if writer is None:
                writer = csv.DictWriter(cf, fieldnames=data.keys())
                writer.writeheader()
            writer.writerow(data)

    print(f"{GREEN}Log successfully exported to CSV at: {csv_file}{RESET}")
