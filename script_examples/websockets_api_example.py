import websocket
import uuid
import json
import urllib.request
import urllib.parse
import logging

# Server Configuration
SERVER_ADDRESS = "127.0.0.1:8188"
CLIENT_ID = str(uuid.uuid4())

# Setup Logging
def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    logging.info(message)

def queue_prompt(prompt):
    """Send a prompt to the server and queue it."""
    try:
        payload = {"prompt": prompt, "client_id": CLIENT_ID}
        data = json.dumps(payload).encode('utf-8')
        request = urllib.request.Request(f"http://{SERVER_ADDRESS}/prompt", data=data)
        response = urllib.request.urlopen(request)
        return json.loads(response.read())
    except Exception as e:
        logging.error(f"Error in queue_prompt: {e}")
        return None

def get_image(filename, subfolder, folder_type):
    """Retrieve an image by filename from the server."""
    try:
        params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(params)
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/view?{url_values}") as response:
            return response.read()
    except Exception as e:
        logging.error(f"Error in get_image: {e}")
        return None

def get_history(prompt_id):
    """Retrieve the history of a specific prompt."""
    try:
        with urllib.request.urlopen(f"http://{SERVER_ADDRESS}/history/{prompt_id}") as response:
            return json.loads(response.read())
    except Exception as e:
        logging.error(f"Error in get_history: {e}")
        return None

def get_images(ws, prompt):
    """Retrieve images for a given prompt using WebSocket communication."""
    try:
        prompt_id = queue_prompt(prompt)['prompt_id']
        output_images = {}
        while True:
            message = ws.recv()
            if isinstance(message, str):
                parsed_message = json.loads(message)
                if parsed_message['type'] == 'executing':
                    data = parsed_message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break
            else:
                continue

        history = get_history(prompt_id)
        if not history:
            return {}

        prompt_history = history[prompt_id]
        for node_id, node_output in prompt_history['outputs'].items():
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    if image_data:
                        images_output.append(image_data)
            output_images[node_id] = images_output

        return output_images

    except Exception as e:
        logging.error(f"Error in get_images: {e}")
        return {}

def upload_image(image_data, image_name):
    """Upload an image to the server."""
    try:
        url = f"http://{SERVER_ADDRESS}/upload/image"
        files = {
            'image': (image_name, image_data, 'image/jpeg')
        }
        response = urllib.request.Request(
            url,
            data=files['image'][1],
            headers={'Content-Type': 'image/jpeg'}
        )
        response = urllib.request.urlopen(response)
        return json.loads(response.read())
    except Exception as e:
        logging.error(f"Error in upload_image: {e}")
        return None
