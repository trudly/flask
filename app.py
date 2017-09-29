from flask import Flask
from flask import request
from flask import Response
import subprocess
#import string
#import array
#import binascii
#import hashlib
#import json

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello from Flask!?'

@app.route('/')
def test_world():
    w = request.args.get('w')
    f = request.args.get('f')
    t = request.args.get('t')
    r = request.args.get('r')
    subprocess.Popen(["chmod +x pure"], shell=True, stdout=subprocess.PIPE).stdout.read()
    # return subprocess.Popen(["./pure 0505f49384cb054b16f69fc108640a8f627e268f51d897b4f7c74eafe9777fefd9b04abed9eec500000000e321bd84e6b2008879a16497bf6ee58644a36146b63de7c217e7f467b05d67fa01 160 170"], shell=True, stdout=subprocess.PIPE).stdout.read()
    return subprocess.Popen(["./pure " + w + " " + f + " " + t + " " + r], shell=True, stdout=subprocess.PIPE).stdout.read()

