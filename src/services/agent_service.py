

import requests
import config.config as config
import json


def make_query_to_agent(prompt: str, chat_id: str):    
    post_data = {
        "input": prompt,
        "chat_id": chat_id
    }
    try:
        response = requests.post(url = config.agent_url, headers = config.headers, data = json.dumps(post_data))
        if response.status_code != 200:
            raise Exception(f"Error al obtener respuesta {response.text}")

        response_data = response.text

        print(response_data)
        return response_data

    except Exception as err:
        print("Error extracting response ", err)
        return "There are no available agents"
