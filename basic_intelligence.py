GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
RESET = '\033[0m'

import json
import requests
import utils
import time

def llm_call_blob(user_query: str, my_model: str = "llama3.2:1b", my_base_url: str = "http://localhost:11434/api/generate/") -> any:
    payload = {
        "model": my_model,
        "prompt": user_query,
        "stream": False
    }

    try:
        start_time = time.time()
        response = requests.post(my_base_url, json=payload)
        end_time = time.time()

        if response.status_code == 200:
            response_data = response.json()
            my_model_response = response_data.get("response", "")
            print(response_data)
            input_tokens = response_data.get("prompt_eval_count", None)
            output_tokens = response_data.get("eval_count", None)


            token_usage = input_tokens+output_tokens

            # Logging
            utils.log_success_plain(my_base_url, user_query, my_model, my_model_response, token_usage)
            utils.log_success_to_file(my_base_url, user_query, my_model, my_model_response, start_time, end_time, token_usage)
            return my_model_response
        else:
            utils.log_error_plain(my_base_url, user_query, my_model, response.status_code, response.text)
            return None

    except requests.RequestException as e:
        utils.log_error_plain(my_base_url, user_query, my_model, "N/A", str(e))
        return None

def llm_call_stream(user_query: str, my_model: str = "llama3.2:1b", my_base_url: str = "http://localhost:11434/api/generate/") -> str:
    payload = {
        "model": my_model,
        "prompt": user_query,
        "stream": True
    }

    try:
        start_time = time.time()
        response = requests.post(my_base_url, json=payload, stream=True)
        end_time = time.time()

        if response.status_code == 200:
            stream_output = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = line.decode("utf-8")
                        json_obj = json.loads(data)
                        token_chunk = json_obj.get("response", "")
                        print(token_chunk, end="", flush=True)
                        stream_output += token_chunk
                    except Exception as decode_err:
                        print(f"{RED}Error decoding stream chunk: {decode_err}{RESET}")

            print()  # Newline after stream output
            utils.log_success_plain(my_base_url, user_query, my_model, stream_output)
            utils.log_success_to_file(my_base_url, user_query, my_model, stream_output, start_time, end_time)
            return stream_output
        else:
            utils.log_error_plain(my_base_url, user_query, my_model, response.status_code, response.text)
            return None

    except requests.RequestException as e:
        utils.log_error_plain(my_base_url, user_query, my_model, "N/A", str(e))
        return None
