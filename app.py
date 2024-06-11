from flask import Flask, request, jsonify
import os
import moviepy.editor as mp
from dotenv import load_dotenv
import tempfile

load_dotenv()

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_mp4_to_mp3():
    # Check if the POST request has the file part
    if 'mp4' not in request.files:
        return jsonify({'error': 'No mp4 part'}), 400
    if 'path' not in request.form:
        return jsonify({'error': 'No path part'}), 400

    file = request.files['mp4']
    
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    path = request.form.get('path')
    base_dir = os.getenv('IMAGES_BASE_DIRECTORY')
    output_file_path = base_dir + path

    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name
        print('temp file name', temp_file.name)
    
    try:
        # Process the video to extract audio
        video = mp.VideoFileClip(temp_file_path)
        audio = video.audio

        # Save the audio to the specified output path
        audio.write_audiofile(output_file_path)

        return jsonify({'message': 'Conversion successful', 'output_path': output_file_path}), 200
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


if __name__ == '__main__':
    from waitress import serve
    port = os.getenv('PORT', '5000')  # Default to port 5000 if not specified
    print('server is running on port : ' + port)
    serve(app, host="0.0.0.0", port=int(port))