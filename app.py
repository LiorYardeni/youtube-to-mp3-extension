import os

import youtube_dl
from os import getcwd, environ, path
from flask import Flask, request
from configuration import get_config
from shutil import copyfile

app = Flask(__name__)
saved_file_directory = get_config('saved_file_directory')
project_path = getcwd()


@app.route('/send_youtube_url', methods=['POST'])
def send_youtube_url():
    content = request.json
    youtube_url = content['youtube_url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(youtube_url)
            video_title = video_info['title']
            if "/" in video_title:
                video_title = video_title.replace("/", "_")
            video_id = video_info['id']
            file_name = '{}-{}{}'.format(video_title, video_id, ".mp3")
            full_download_path = '{}/{}'.format(project_path, file_name)
            full_download_path_ = full_download_path.replace("|", "_")
            saved_file_path = '{}{}'.format(saved_file_directory, file_name)
            copyfile(full_download_path_, saved_file_path)
            os.remove(full_download_path_)
            return "{} downloaded successfully".format(video_title)
        except:
            return "Video is unavailable"


@app.route('/health', methods=['GET'])
def health():
    return "OK"


if __name__ == '__main__':
    port = int(environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', use_reloader=True, port=port)
