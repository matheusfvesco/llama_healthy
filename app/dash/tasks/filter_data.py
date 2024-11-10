# dash/tasks/filter_data.py

import requests
from datetime import datetime, timedelta
import pandas as pd

# Function to interpret the prompt for time filtering using flexible categorization
def interpret_time_filter(prompt, api_key):
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": f"classifique esse prompt em 'mês atual', 'mês passado', or 'todos os dados': {prompt}"}
        ],
        "max_tokens": 15
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        # Extract the interpretation (e.g., "current month", "last month", or "all data")
        interpretation = response.json()["choices"][0]["message"]["content"].strip().lower()
        return interpretation
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to filter data based on interpreted category
def filter_data_by_time(data, time_filter):

    print(time_filter)
    current_date = datetime.now()

    print(data['DT_NOTIFIC'].head())
    
    if "mês passado" in time_filter.lower():
        # Filter for last month
        first_day_last_month = (current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_last_month.replace(day=1) + timedelta(days=32)
        last_day_last_month = last_day_last_month.replace(day=1) - timedelta(days=1)
        filtered_data = data[(data['DT_NOTIFIC'] >= first_day_last_month.strftime('%Y-%m-%d')) &
                             (data['DT_NOTIFIC'] <= last_day_last_month.strftime('%Y-%m-%d'))]

    elif "mês atual" in time_filter.lower():
        # Filter for current month
        first_day_current_month = current_date.replace(day=1)
        filtered_data = data[data['DT_NOTIFIC'] >= first_day_current_month.strftime('%Y-%m-%d')]
    
    else:
        # Default case: return all data if no valid time filter found
        filtered_data = data
    
    return filtered_data
