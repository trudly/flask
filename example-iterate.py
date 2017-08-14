from pyzceqsolver import Solver
import string
import array
import binascii
import hashlib

s = Solver()

org_solution = [123] * 512
min = s.list_to_minimal(org_solution)
back = s.minimal_to_list(min)
assert back == org_solution
solLen = "fd4005"
#targetHex = "0000000000000000000000000000000000000000000000000000000000000400"
#targetHex = "0000000000000000000000000000000000000000000000000000000000004000"
targetHex = "0040000000000000000000000000000000000000000000000000000000000000"
#data = "04000000bba85f685805d66fe980945979ebd50b760a6914fd01321283979a0f000000008cd62e249a8549168278a5f349ea23ae9202726496c28ddb7465c8f4b361f9200000000000000000000000000000000000000000000000000000000000000000367e9159d7871d1c0000000089000000000000000000000000000000000000000000000000000000"
#data = "04000000480518c1779651be94531478593bb46c355612378116ef81a8858f0200000000e4adc3a743e5877d6959a2717d13fccf92e08664b3a691c9286426b431abc2db0000000000000000000000000000000000000000000000000000000000000000b57e915975ac1c1c0000000001010000000000000000000000000000000000000000000000000000"
w = "04000000bba85f685805d66fe980945979ebd50b760a6914fd01321283979a0f000000008cd62e249a8549168278a5f349ea23ae9202726496c28ddb7465c8f4b361f9200000000000000000000000000000000000000000000000000000000000000000367e9159d7871d1c00000000"
f = "80"
#t = "a0"
t = "f8"

def isProperSolution(diff, target):
    for i in range(0, 32):
        #print "Compare %d vs %d" % (diff[32 - 1 - i], target[i])
        if diff[32 - 1 - i] < target[i]:
            return True
        if diff[32 - 1 - i] > target[i]:
            return False

#for character in string.printable:
def findSolution(w, f, t):
    fInt = int(f, base=16);
    tInt = int(t, base=16);
    for nonceInt in range(fInt, tInt):

        dataNonced = w + "{:02x}".format(nonceInt)
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
                    print respList
                    return
                    #print "Accepted solution: %s" % solHex
                    #print "diff is"
                    #print diffFinalHex
                    #print [int(diffFinalHex[i:i+2],16) for i in range(0,len(diffFinalHex),2)]
                    #print [int(targetHex[i:i+2],16) for i in range(0,len(targetHex),2)]
                    #print ""

findSolution(w, f, t)
