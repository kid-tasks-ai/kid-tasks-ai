import requests
import json

# Define the JSON payload
payload = {
    "child_description": {
        "age": 8,
        "gender": "male",
        "interests": "interests description"
    },
    "tasks_description": {
        "chore_tasks": ["make the bed", "do dishes"],
        "creative_tasks": {
            "amount": 3,
            "topics": ["space adventure"]
        }
    }
}

# URL of the FastAPI app running in Docker
url = "http://localhost:8010/generate_tasks"

# Send GET request with JSON payload
response = requests.get(url, json=payload)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
