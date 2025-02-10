from flask import Flask, request, jsonify
import websocket
from script_examples.websockets_api_example import setup_logger, get_images, upload_image, SERVER_ADDRESS, CLIENT_ID
import logging

app = Flask(__name__)
setup_logger()

@app.route('/process-prompt', methods=['POST'])
def process_prompt():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # WebSocket bağlantısı oluştur
        ws = websocket.WebSocket()
        ws.connect(f"ws://{SERVER_ADDRESS}/ws?clientId={CLIENT_ID}")
        
        # Promptu işle ve görüntüleri al
        images = get_images(ws, prompt)
        ws.close()
        
        return jsonify({'images': images})
    
    except Exception as e:
        logging.error(f"Error processing prompt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
            
        image_file = request.files['image']
        image_data = image_file.read()
        image_name = image_file.filename
        
        result = upload_image(image_data, image_name)
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error uploading image: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000) 
