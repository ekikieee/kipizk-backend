from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import sys
import traceback

app = Flask(__name__)
CORS(app,
     resources={r"/*": {"origins": "*"}},
     allow_headers=["Content-Type"],
     methods=["GET", "POST", "OPTIONS"])

remove_func = None

def get_remove():
    global remove_func
    if remove_func is None:
        print("Loading rembg model...", flush=True)
        from rembg import remove as _remove
        remove_func = _remove
        print("Model loaded OK", flush=True)
    return remove_func

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'KiPiZK Background Removal API',
        'model_loaded': remove_func is not None
    })

@app.route('/api/remove-bg', methods=['POST'])
def remove_background():
    try:
        rm = get_remove()

        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400

        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

        print(f"Processing image: {input_image.size}", flush=True)
        output_image = rm(input_image)
        print("Processing done", flush=True)

        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_bytes = output_buffer.getvalue()
        output_base64 = base64.b64encode(output_bytes).decode('utf-8')

        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{output_base64}'
        })

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
