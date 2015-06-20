from ethereum import tester
from ethereum import utils
serpent_contract = """
extern solidity: [sub2:[]:i]

def main(a):
    return(a.sub2() * 2)

def sub1():
    return(5)

"""

solidity_contract = """
contract serpent { function sub1() returns (int256 y) {} }

contract zoo {
    function main(address a) returns (int256 y) {
        y = serpent(a).sub1() * 2;
    }
    function sub2() returns (int256 y) {
        y = 7;
    }
    function sub3(address a) returns (address b) {
        b = a;
    }
}
"""


def test_interop():
    if 'solidity' not in tester.languages:
        return
    s = tester.state()
    c1 = s.abi_contract(serpent_contract)
    c2 = s.abi_contract(solidity_contract, language='solidity')  # should be zoo
    assert c1.sub1() == 5
    assert c2.sub2() == 7
    assert c2.sub3(utils.encode_hex(c2.address)) == utils.encode_hex(c2.address)
    assert c1.main(c2.address) == 14
    assert c2.main(c1.address) == 10
