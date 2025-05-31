import requests
import json
import base64
import config.config as config  
from uuid import UUID

# Function to send a query to the agent
def make_query_to_agent(chat_id: str, prompt: str, engine: str, image_path: str = None):    
    post_data = {
        "input": prompt,
        "chat_id": chat_id,
        "engine": engine,
    }

    try:
        if image_path:
            post_data["image_path"] = image_path

        response = requests.post(
            url=config.agent_url,
            headers=config.headers,
            data=json.dumps(post_data)
        )

        if response.status_code != 200:
            raise Exception(f"Error al obtener respuesta {response.text}")

        response_data = response.text
        print(response_data)
        return response_data

    except Exception as err:
        print("Error extracting response:", err)
        return "There are no available agents"
