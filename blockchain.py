from hashlib import sha256
import os

from numpy import diff

class Block:
    
    def __init__(self,bytes):
        self.bytes = bytes
        
    def prevHash(self):
        return self.bytes[0:32] # First 32 bytes (265 bits) are the prev hash
    
    def transations(self):
        return self.bytes[36:1000-32] # All transactions
    
    def is_valid(self,difficulty):
        hash = bytes(self.hash())
        number = int.from_bytes(hash,'big') >> 256-difficulty
        return sha256(self.bytes[0:-32]).digest() == hash and number == 0
    
    def nonce(self):
        print(len(self.bytes[-32:-28]))
        return self.bytes[-36:-32] # Next 4 bytes are the nonce to achieve the difficulty
    
    def hash(self):
        return self.bytes[-32:]
    
    

def mine(b,difficulty):
    number = 1
    nonce = 1
    shift = 256 - difficulty
    while number != 0:
        nonce = bytearray(os.urandom(4))
        tempBlock = b + nonce
        h = sha256(tempBlock).digest()
        number = int.from_bytes(h,'big') >> shift
    return nonce


if __name__ == "__main__":
    randomBlock = bytearray(os.urandom(1000-36))
    blockSolution = mine(randomBlock,15)
    blockBytes = randomBlock + blockSolution + bytearray(sha256(randomBlock+blockSolution).digest())
    
    
    
    b = Block(bytearray(blockBytes))
    
    print(b.is_valid(15))
    print(sha256(randomBlock+blockSolution).digest().hex())