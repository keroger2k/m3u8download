import os
import requests
import m3u8
import ffmpeg
from flask import Flask, request, jsonify, send_from_directory
from urllib.parse import urlparse

app = Flask(__name__)
DOWNLOAD_DIR = 'downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    m3u8_url = data.get('url')

    if not m3u8_url:
        return jsonify({'error': 'm3u8 URL is required'}), 400

    try:
        # Load the m3u8 playlist
        playlist = m3u8.load(m3u8_url)

        segment_urls = []
        for segment in playlist.segments:
            segment_urls.append(segment.uri)

        # Download all segments
        segment_files = []
        for i, url in enumerate(segment_urls):
            # Handle relative URLs
            if not url.startswith('http'):
                base_url = m3u8_url.rsplit('/', 1)[0]
                url = f"{base_url}/{url}"

            r = requests.get(url, stream=True)
            segment_file = os.path.join(DOWNLOAD_DIR, f'segment_{i}.ts')
            with open(segment_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            segment_files.append(segment_file)

        # Combine segments with ffmpeg
        output_filename = os.path.join(DOWNLOAD_DIR, 'output.mp4')

        # Create a file list for ffmpeg
        with open('file_list.txt', 'w') as f:
            for segment_file in segment_files:
                f.write(f"file '{segment_file}'\n")

        # Use ffmpeg to concatenate the files
        (
            ffmpeg
            .input('file_list.txt', format='concat', safe=0)
            .output(output_filename, c='copy')
            .run(overwrite_output=True)
        )

        # Clean up segment files and file list
        for segment_file in segment_files:
            os.remove(segment_file)
        os.remove('file_list.txt')

        return jsonify({'download_url': f'/downloads/output.mp4'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
