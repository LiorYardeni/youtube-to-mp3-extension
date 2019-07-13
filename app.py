import youtube_dl
import os
from flask import Flask, request

app = Flask(__name__)


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
            ydl.download([youtube_url])
            return "{} downloaded successfully".format(video_title)
        except:
            return "Video is unavailable"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', use_reloader=True, port=port)
