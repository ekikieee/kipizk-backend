from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'KiPiZK Background Removal API',
        'version': '1.0.0'
    })

@app.route('/api/remove-bg', methods=['POST'])
def remove_background():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        # Get base64 image
        image_data = data['image']
        
        # Remove data:image/...;base64, prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        
        # Open image
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # Remove background
        output_image = remove(input_image)
        
        # Convert to PNG bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_bytes = output_buffer.getvalue()
        
        # Encode to base64
        output_base64 = base64.b64encode(output_bytes).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{output_base64}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
