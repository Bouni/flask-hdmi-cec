#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import threading
from flask import Flask, jsonify
from flask_cors import CORS

lock = threading.Lock()

class CEC(threading.Thread):

    STATES = {
        "power status: standby": 0,
        "power status: on": 1,
        "power status: in transition from on to standby": 2,
        "power status: in transition from standby to on": 3,
        "power status: unknown": 5
    }

    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
        self._command = None
        self._state = {"text": "unknown", "value": 5}

    def get_state(self):
        return {"state": self._state}

    def on(self):
        self._command = "on"
        return {"state": self._state}

    def off(self):
        self._command = "off"
        return {"state": self._state}

    def stop(self):
        self._running = False

    def _cec_command(self, command):
        p1 = subprocess.Popen(
            'echo "{} 0"'.format(command),
            stdout=subprocess.PIPE,
            shell=True)
        p2 = subprocess.Popen(
            'cec-client -s -d 1',
            stdin=p1.stdout,
            stdout=subprocess.PIPE,
            shell=True)
        output, err = p2.communicate()
        for k, v in self.STATES.items():
            if k in str(output):
                return {"text": k[14:], "value": v}
        return self._state 

    def run(self):
        while self._running:
            if self._command == "on":
                with lock:
                    self._state = self._cec_command("on")
                    self._command = None
            elif self._command == "off":
                with lock:
                    self._state = self._cec_command("standby")
                    self._command = None
            else:
                with lock:
                    self._state = self._cec_command("pow")


app = Flask(__name__)
CORS(app)
app.config["CEC"] = CEC()


@app.before_first_request
def init():
    app.config["CEC"].start()


@app.route("/")
def state():
    return jsonify(app.config["CEC"].get_state())


@app.route("/on")
def on():
    return jsonify(app.config["CEC"].on())


@app.route("/off")
def off():
    return jsonify(app.config["CEC"].off())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4321, use_reloader=False)
