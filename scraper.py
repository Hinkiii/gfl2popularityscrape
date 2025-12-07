import requests
import json
import csv
import time
import os

API_URL = "https://gf2-gameworldrank-us-api.sunborngame.com/activity/rank"
POPULARITY_FILENAME = "gun_popularity_history.csv"
SCORE_FILENAME = "gun_score_history.csv"
FIELDNAMES = ["timestamp", "gun_id", "rank", "point"]

def fetch_and_parse_data(url: str) -> tuple[list, list]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        current_time_unix = time.time()
        
        if data.get("code") == 0 and "data" in data:
            api_data = data["data"]
            
            popularity_list = api_data.get("popularity_rank_list", [])
            popularity_records = [{
                "timestamp": current_time_unix,
                "gun_id": item["gun_id"],
                "rank": item["rank"],
                "point": item["point"]
            } for item in popularity_list]

            score_list = api_data.get("score_rank_list", [])
            score_records = [{
                "timestamp": current_time_unix,
                "gun_id": item["gun_id"],
                "rank": item["rank"],
                "point": item["point"]
            } for item in score_list]
            
            return popularity_records, score_records
            
        else:
            return [], []

    except requests.exceptions.RequestException:
        return [], []
    except json.JSONDecodeError:
        return [], []

def save_data_to_csv(records: list, filename: str, fieldnames: list):
    if not records:
        return

    file_exists = os.path.exists(filename)
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerows(records)

    except IOError:
        pass

if __name__ == "__main__":
    popularity_data, score_data = fetch_and_parse_data(API_URL)
    
    if popularity_data:
        save_data_to_csv(popularity_data, POPULARITY_FILENAME, FIELDNAMES)
        
    if score_data:
        save_data_to_csv(score_data, SCORE_FILENAME, FIELDNAMES)
