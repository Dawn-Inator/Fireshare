import os, re
from flask import Blueprint, request, Response, jsonify
from flask_login import logout_user, current_user
from flask_cors import CORS
from . import db

api = Blueprint('api', __name__)

CORS(api, supports_credentials=True)

# sample.mp4 is just a silent spinning earth
# sample2.mp4 is a larger video with sound and burned in subtitles

def get_video_path(id):
    # db lookup to get path to mp4
    return 'app/server/test_videos/{id}.mp4'.format(id=id)

@api.route('/api/video/details', methods=["GET"])
def get_video_details():
    # db lookup and get the details title/views/etc
    video_id = request.args['id']
    return jsonify(
        title="This is just a temporary title",
        views=9001
    )

@api.route('/api/video')
def get_video():
    # for testing ids are just the name of the sample video until
    # we have the videos added to a db table
    video_id = request.args.get('id')
    video_path = get_video_path(video_id)
    file_size = os.stat(video_path).st_size
    start = 0
    length = 10240

    range_header = request.headers.get('Range', None)
    if range_header:
        m = re.search('([0-9]+)-([0-9]*)', range_header)
        g = m.groups()
        byte1, byte2 = 0, None
        if g[0]:
            byte1 = int(g[0])
        if g[1]:
            byte2 = int(g[1])
        if byte1 < file_size:
            start = byte1
        if byte2:
            length = byte2 + 1 - byte1
        else:
            length = file_size - start

    with open(video_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)

    rv = Response(chunk, 206, mimetype='video/mp4', content_type='video/mp4', direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return rv

@api.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response