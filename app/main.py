# -*- coding: utf-8 -*-
"""
    jQuery Example
    ~~~~~~~~~~~~~~

    A simple application that shows how Flask and jQuery get along.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, jsonify, render_template, request
import sys
import multiprocessing
from werkzeug import secure_filename
from controller.commander import Commander
import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/upload/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
app.debug = True
new_upload_filename = os.path.join(app.config['UPLOAD_FOLDER'], "ip.txt")

@app.route('/parse_status')
def parse_status():
    print "Getting status----------------"
    return jsonify(str(Commander().get_parse_status()))

@app.route('/parse')
def parse():
    filename = request.args.get('filename')
    d = multiprocessing.Process(name='daemon', target=parse_task)
    d.daemon = True
    d.start()
    print "PID = " + str(d.pid)

    # c = Commander()
    # c.parse(new_upload_filename)
    print "Starting"
    return jsonify("Started")

def parse_task():
    print "Starting task!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    c = Commander()
    c.reset(1,0)
    c.reset(2, 0)
    c.parse(new_upload_filename)
    c.reset(1,-1)
    c.reset(2, 0)
    sys.exit(0)

@app.route('/find')
def find():
    a = request.args.get('a')

    c = Commander()
    r = c.run(a)
    dict = {}
    dict['result'] = r
    return jsonify(r)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   print "Uploading a file"
   if request.method == 'POST':
      f = request.files['file']
      c = Commander()
      c.reset(1,0)
      c.reset(2, 0)
      print "In Post: " + secure_filename(f.filename)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      os.rename(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), new_upload_filename)
      print "Done!!"
      return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
#    app.run()
    c = Commander()
    # c.rdap_test('174.16.66.242')
    c.parse(sys.argv[1])


    # print sys.argv[1]
    # r = c.run(sys.argv[1])
    # dict = {}
    # dict['result'] = r
    # print dict['result'][0]['city']


