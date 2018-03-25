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

import os
import speech_recognition as sr
from flask import Flask, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

project_path = '/home/jordi/sc/cmusphinx-models-jordi/'

def get_model_path(language=None):
    language_path = os.path.join(project_path,'ca-ca')
    hmm_path = os.path.join(language_path,'acoustic-model')
    lm_file = os.path.join(language_path,'language-model.lm.bin')
    dict_file = os.path.join(language_path,'pronounciation-dictionary.dict')
    for prequisit in [language_path, hmm_path, lm_file, dict_file]:
        if not os.path.exists(prequisit):
            raise IOError('%s does not exits'%prequisit)
    return hmm_path, lm_file, dict_file

def recognize(audio_file):
    language='ca-ca'
    hmmd, lmd, dictd = get_model_path(language)
    language_tuple = (hmmd, lmd, dictd)

    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    return r.recognize_sphinx(audio,language=language_tuple)

#  curl -X POST -F 'file=@test_ca-ca.wav' http://127.0.0.1:5000/recognize/
@app.route('/recognize/', methods=['POST'])
def recognize_api():

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No filename'

    filename = secure_filename(file.filename)
    file.save(filename)
    text = recognize(filename)
    return "text:" + text

if __name__ == '__main__':
    app.debug = True
    app.run()
