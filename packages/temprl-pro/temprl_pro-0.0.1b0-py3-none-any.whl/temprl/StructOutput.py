import json

import requests

def fetch_data_from_api(data_id: str, query: str, api_key: str, max_tokens: int = 1000) -> dict:
    print("[DEBUG] fetch_data_from_api called with data_id:", data_id, "query:", query, "api_key:", api_key, "max_tokens:", max_tokens)
    url = "https://api.temprl.pro/get-data"  # Adjust the URL if needed

    payload = {"id": data_id, "data": query, "api": api_key, "max_tokens": max_tokens}
    print("[DEBUG] Payload for request:", payload)
    
    try:
        response = requests.post(url, json=payload)
        print("[DEBUG] Response status code:", response.status_code)
        response.raise_for_status()  # Raise an error for bad responses
        response_json = response.json()
        print("[DEBUG] Response JSON:", response_json)
        return response_json  # Return the JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"[ERROR] HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"[ERROR] An error occurred: {err}")

def get_json(template_id: str, query: str, api_key: str, max_tokens: int = 1000) -> dict:
    data = fetch_data_from_api(template_id, query, api_key, max_tokens)
    print(data)
    if data:
        return data["data"][0]
    return None