from pyzceqsolver import Solver
import string
import binascii
import hashlib

s = Solver()

org_solution = [123] * 512
min = s.list_to_minimal(org_solution)
back = s.minimal_to_list(min)
assert back == org_solution

def isProperSolution(diff, target):
    for i in range(0, 32):
        print "Compare %d vs %d" % (diff[32 - 1 - i], target[i])
        if diff[32 - 1 - i] < target[i]:
            return True
        if diff[32 - 1 - i] > target[i]:
            return False

#for character in string.printable:
for character in range(0, 1):
    data = "040000004c6cf5c1134af4192065efa39bf967ad01ce8ecc2308538769c1bd0c000000004a6fe35ddfaa83d4f3e32d9985e702a2c5dbef27a260993d0a2727d03b647368000000000000000000000000000000000000000000000000000000000000000033419159ae87211c0c00033e84000000000000000000000000000000000000000000000000000000"

#    block_header = character * 140
    block_header = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

#    block_header = b'04000000eca010e534b9ff4a8089186313c87e7926fefd3de7d6fb051032bf1c00000000cda88e793ddcd297f91c5131bfa6578d0c0df81a18a45c253c9e838adb6bbc6a000000000000000000000000000000000000000000000000000000000000000051309159c3eb1d1c0c00033989000000000000000000000000000000000000000000000000000000'

    n = s.find_solutions(block_header)
    print n, 'solution(s) found for "%s"' % character

    for e in range(n):
        solution = s.get_solution(e)
        assert len(solution) == 1344

        # Try to validate a given solution
        # -1 = internal error, 0 = invalid solution, 1 = valid solution

        result = s.validate_solution(block_header, solution)
        if result != 1:
            print "Error: invalid solution (%d)" % result

        result = s.validate_solution(block_header, solution[::-1])
        if result != 0:
            print "Error: solution should be rejected (%d)" % result
        if result == 0:
            solHex = binascii.hexlify(solution)
            fullBlockHex = data + 'fd4005' + solHex
            #print fullBlockHex
            diff = hashlib.sha256(bytearray.fromhex(fullBlockHex)).digest()
            diffFinal = hashlib.sha256(diff)
            diffFinalHex = diffFinal.hexdigest()
            #targetHex = "0000000000000000000000000000000000000000000000000000000000000100"
            targetHex = "0001000000000000000000000000000000000000000000000000000000000000"
            print "Accepted solution: %s" % solHex
            print "diff is"
            print diffFinalHex
            print [int(diffFinalHex[i:i+2],16) for i in range(0,len(diffFinalHex),2)]
            print [int(targetHex[i:i+2],16) for i in range(0,len(targetHex),2)]
            print isProperSolution([int(diffFinalHex[i:i+2],16) for i in range(0,len(diffFinalHex),2)], [int(targetHex[i:i+2],16) for i in range(0,len(targetHex),2)])
            print ""
