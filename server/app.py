from flask import Flask, request, jsonify, send_from_directory
from PIL import Image, ImageFilter
import os
from database import init_db, insert_image_metadata

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static")
PROCESSED_FOLDER = os.path.join(os.path.dirname(__file__), "processed")


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    image = Image.open(filepath)
    processed = image.filter(ImageFilter.CONTOUR)
    processed_filename = f"processed_{filename}"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    processed.save(processed_path)

    insert_image_metadata(filename, 'CONTOUR')

    return jsonify({
        'original': f'/static/{filename}',
        'processed': f'/processed/{processed_filename}'
    })

@app.route('/static/<path:filename>')
def get_original(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/processed/<path:filename>')
def get_processed(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
