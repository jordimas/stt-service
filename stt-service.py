#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2018 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import tempfile
import datetime
import json
from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from recognizer import Recognizer
from usage import Usage

app = Flask(__name__)

#  curl -X POST -F 'file=@test_ca-ca.wav' http://127.0.0.1:5000/recognize/
@app.route('/recognize/', methods=['POST'])
def recognize_api():

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No filename'

    time = datetime.datetime.now()
    try:
        with tempfile.NamedTemporaryFile() as temp_file:
            recognizer = Recognizer()
            filename = temp_file.name
            file.save(filename)
            text = recognizer.get_text(filename)
            used = datetime.datetime.now() - time
            usage = Usage()
            usage.log()
            return "Text reconegut: [{0}] - temps usat {1}".format(text, used)
    except ValueError as e:
        return ("No és un fitxer d'àudio en format PCM WAV, AIFF/AIFF-C o FLAC ", 400)

@app.route('/recognize/stats/', methods=['GET'])
def stats():
    requested = request.args.get('date')
    date_requested = datetime.datetime.strptime(requested, '%Y-%m-%d')
    usage = Usage()
    calls = usage.get_stats(date_requested)

    result = {}
    result['calls'] = calls
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

def json_answer(data):
    resp = Response(data, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
