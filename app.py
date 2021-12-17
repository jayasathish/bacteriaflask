import os
from flask import Flask, Response, request, abort, send_from_directory, render_template
from PIL import Image
from io import StringIO

app = Flask(__name__, template_folder='templates')
WIDTH = 300
HEIGHT = 450


@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory('.', filename)


@app.route('/')
@app.route('/bacteria')
def index():
    images = []
    for root, dirs, files in os.walk('.'):
        for filename in [os.path.join(root, name) for name in files]:
            if not filename.endswith('.jpg'):
                continue
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect

            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename,
                "name":"test"
            })

    return render_template('bacteria.html', **{'images': images})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)