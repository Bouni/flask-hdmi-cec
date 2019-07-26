#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import subprocess
import threading

class CEC(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
        self._command = None
        self._state = "unknown"

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
        p1 = subprocess.Popen('echo "{} 0"'.format(command), stdout=subprocess.PIPE, shell=True)
        p2 = subprocess.Popen('cec-client -s -d 1', stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
        output, err = p2.communicate()
        for s in ("unknown","standby","on"):
            if s in str(output):
                return s
        return "Undefined output: {}".format(output)

    def run(self):
        while self._running:
            if self._command == "on":
                self._state = self._cec_command("on")
                self._command = None
            elif self._command == "off":
                self._state = self._cec_command("standby")
                self._command = None
            else:
                self._state = self._cec_command("pow")


app = Flask(__name__)
app.config["CEC"] = CEC()

@app.before_first_request
def init():
    app.config["CEC"].start()

@app.route("/")
def state():  
    return app.config["CEC"].get_state()

@app.route("/on")
def on():    
    return app.config["CEC"].on()

@app.route("/off")
def off():    
    return app.config["CEC"].off()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4321, use_reloader=False)
