import requests
import json
import base64
import config.config as config  
from uuid import UUID


def leave_room(chat_id: UUID):    
    post_data = {
        "chat_id": str(chat_id)
    }

    try:

        response = requests.post(
            url=config.leave_room_url,
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
        return "Error leaving room"
