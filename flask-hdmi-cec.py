#!/usr/bin/env python3.5
#-*- coding: utf-8 -*-

from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/state')
def status():
    p1 = subprocess.Popen('echo "pow 0"', stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen('cec-client -s -d 1', stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
    output, err = p2.communicate()
    for n,s in enumerate(["standby","on","unknown"]):
        if s in str(output):
            return jsonify({'state':s, 'number':n})
    print("Unknown state of {0} received".format(output))
    return jsonify({'state':'unknown', 'number':-1})

@app.route('/on')
def on():
    p1 = subprocess.Popen('echo "on 0"', stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen('cec-client -s -d 1', stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
    output, err = p2.communicate()
    return jsonify({'success':True})

@app.route('/off')
def off():
    p1 = subprocess.Popen('echo "standby 0"', stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen('cec-client -s -d 1', stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
    output, err = p2.communicate()
    return jsonify({'success':True})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=4321)
