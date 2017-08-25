from flask import Flask
from flask import request
from flask import Response
from pyzceqsolver import Solver
import subprocess
import string
import array
import binascii
import hashlib
import json

s = Solver()

org_solution = [123] * 512
min = s.list_to_minimal(org_solution)
back = s.minimal_to_list(min)
assert back == org_solution
solLen = "fd4005"

s = Solver()

org_solution = [123] * 512
min = s.list_to_minimal(org_solution)
back = s.minimal_to_list(min)
assert back == org_solution
solLen = "fd4005"

def isProperSolution(diff, target):
    for i in range(0, 32):
        #print "Compare %d vs %d" % (diff[32 - 1 - i], target[i])
        if diff[32 - 1 - i] < target[i]:
            return True
        if diff[32 - 1 - i] > target[i]:
            return False

def findSolution(w, f, t, targetHex):
    fInt = int(f, base=16);
    tInt = int(t, base=16);
    for nonceInt in range(fInt, tInt):

        dataNonced = w + "{:02x}".format(nonceInt)
        if nonceInt > 255:
            dataNonced = w + "{:04x}".format(nonceInt)
        data = dataNonced.ljust(280, '0')

        block_header = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

        n = s.find_solutions(block_header)
        #print n, 'solution(s) found for "%s"' % hex(nonceInt)
        #print n, 'solution(s) found for "%s"' % "{:02x}".format(nonceInt)

        for e in range(n):
            solution = s.get_solution(e)
            assert len(solution) == 1344

            result = s.validate_solution(block_header, solution)
            if result != 1:
                print "Error: invalid solution (%d)" % result

            result = s.validate_solution(block_header, solution[::-1])
            if result != 0:
                print "Error: solution should be rejected (%d)" % result
            if result == 0:
                solHex = binascii.hexlify(solution)
                fullBlockHex = data + solLen + solHex
                #print fullBlockHex
                diff = hashlib.sha256(bytearray.fromhex(fullBlockHex)).digest()
                diffFinal = hashlib.sha256(diff)
                diffFinalHex = diffFinal.hexdigest()
                if isProperSolution([int(diffFinalHex[i:i+2],16) for i in range(0,len(diffFinalHex),2)], [int(targetHex[i:i+2],16) for i in range(0,len(targetHex),2)]):
                    respList = []
                    respList.append("{:02x}".format(nonceInt).ljust(56, '0'))
                    respList.append(solLen + solHex)
                    return respList



app = Flask(__name__)

@app.route('/')
def qqruqu():
    w = request.args.get('w')
    f = request.args.get('f')
    t = request.args.get('t')
    targetHex = request.args.get('r')
    solution = findSolution(w, f, t, targetHex)
    if solution is None:
        return Response('{"response": null}', status = 404, mimetype='application/json')
    dump = json.dumps(solution)
    return Response('{"response": ' + dump + '}', mimetype='application/json')

@app.route('/hello')
def hello_world():
    return 'Hello from Flask!?'

@app.route('/test')
def test_world():
    subprocess.Popen(["chmod +x", "pure"], shell=True, stdout=subprocess.PIPE).stdout.read()
    return subprocess.Popen(["./pure", "0505f49384cb054b16f69fc108640a8f627e268f51d897b4f7c74eafe9777fefd9b04abed9eec500000000e321bd84e6b2008879a16497bf6ee58644a36146b63de7c217e7f467b05d67fa01", "160", "170"], shell=True, stdout=subprocess.PIPE).stdout.read()

