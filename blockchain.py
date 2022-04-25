from hashlib import sha256
import os

from numpy import diff
from datetime import datetime,timedelta

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
        return self.bytes[-36:-32] # Next 4 bytes are the nonce to achieve the difficulty
    
    def hash(self):
        return self.bytes[-32:]
    
    def __str__(self):
        str = "\tBlock :" + "\n" \
         + "\tPrev Hash: " + self.prevHash().hex() + "\n" \
        + "\tHash: " + self.hash().hex() + "\n"  \
        + "\tBlock solution : " + self.nonce().hex() + "\n" 
        #+ "Transaction : " + self.transations().hex() + "\n" 
        return str

'''
The Blockchain class contains an array of blocks
'''    
class Blockchain:
    
    '''
    Init the blockchain with an empty array and the diffulty of 10
    '''
    def __init__(self):
        self.blockchain = []
        self.difficulty = 20
        self.initHash = bytearray(b'0' * 32)
        self.creationDate = datetime.now()
    
    '''
    submit_block use to add a block to the block chain, only if the block chain is valid, 
    the previous hash of the block is the hash of the last block of the block chain
    and the block is valid
    '''
    def submitBlock(self,block):
        if self.is_valid():
            lastHash = self.lastHash()
            if block.prevHash() == lastHash:
                pass
                if block.is_valid(self.difficulty):
                    self.blockchain.append((block,datetime.now(),self.difficulty))
                    
                    try:
                        if self.blockchain[-1][1] - self.blockchain[-2][1] > timedelta(seconds=10):
                            self.difficulty -= 1
                            print(f"The difficulty has been decreased to {self.difficulty}")
                        elif self.blockchain[-1][1] - self.blockchain[-2][1] < timedelta(seconds=10):
                            self.difficulty += 1
                            print(f"The difficulty has been increased to {self.difficulty}")
                        print(f"It took {(self.blockchain[-1][1] - self.blockchain[-2][1]).seconds} s to mine the block")
                    except IndexError as e:
                        pass
                
    
    '''
    is_valid check if the block chain is valid.
    '''
    def is_valid(self):
        prevHash = self.initHash # 0 * 32 is the initial hash
        for b,_,difficulty in self.blockchain:
            if b.prevHash() == prevHash:
                if b.is_valid(difficulty):
                    prevHash = b.hash()
                else:
                    return False
            else:
                return False
        return True
    
    
    def getBlockToMine(self):
        return self.lastHash() + bytearray(os.urandom(1000-36 - 32))
            

    def lastBlock(self):
        return self.blockchain[-1]
    
    def lastHash(self):
        if len(self.blockchain) == 0:
            return self.initHash
        return self.lastBlock()[0].hash()
    
    def __str__(self):
        string = f"The blockchain is {len(self.blockchain)} blocks long\n"
        for i,b in enumerate(self.blockchain):
            string += f"Block {i}:\n"
            string += f"{b[0]}\n"
        
        return string
        
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
    
    bc = Blockchain()
    for i in range(100):
        print(f"mining block {i}")
        nextBlock = bc.getBlockToMine()
        blockSolution = mine(nextBlock,bc.difficulty)
        blockBytes = bytearray(nextBlock + blockSolution + bytearray(sha256(nextBlock+blockSolution).digest()))

        bc.submitBlock(Block(blockBytes))
        print(f"Solution found block submited")
    
    
    print(bc)
    
    