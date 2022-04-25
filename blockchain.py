'''
Bitcoin simulation - Security course (2022)
@author: Boegli Lenny and Izzo Valentino
Python version: 3.9.2 
'''

from hashlib import sha256
import os
from datetime import datetime,timedelta

'''
The Block class represents a block in the blockchain.
''' 
class Block:
    
    '''
    Init the block with the informations bytes
    '''
    def __init__(self,bytes):
        self.bytes = bytes
    
    '''
    Return the previous hash in the blockchain.
    '''
    def prevHash(self):
        return self.bytes[0:32] # First 32 bytes (265 bits) are the prev hash
    
    '''
    Return all the transactions of the block.
    '''
    def transations(self):
        return self.bytes[36:1000-32] # All transactions
    
    '''
    Check if the block is valid.
    '''
    def is_valid(self,difficulty):
        hash = bytes(self.hash())
        number = int.from_bytes(hash,'big') >> 256-difficulty
        return sha256(self.bytes[0:-32]).digest() == hash and number == 0
    
    '''
    Return the nonce of the block.
    '''
    def nonce(self):
        return self.bytes[-36:-32] # Next 4 bytes are the nonce to achieve the difficulty
    
    '''
    Return the hash of the block.
    '''
    def hash(self):
        return self.bytes[-32:]
    
    '''
    Display the information of the block.
    '''
    def __str__(self):
        str = "\tBlock :" + "\n" \
         + "\tPrev Hash: " + self.prevHash().hex() + "\n" \
        + "\tHash: " + self.hash().hex() + "\n"  \
        + "\tBlock solution : " + self.nonce().hex() + "\n"
        return str

'''
The Blockchain class contains an array of blocks
'''    
class Blockchain:
    
    '''
    Init the blockchain with an empty array, the diffulty of 10, the initial hash and the creation date
    '''
    def __init__(self):
        self.blockchain = []
        self.difficulty = 10
        self.initHash = bytearray(b'0' * 32)
        self.creationDate = datetime.now()
    
    '''
    Use to add a block to the block chain, only if the block chain is valid, 
    the previous hash of the block is the hash of the last block of the block chain
    and the block is valid
    '''
    def submitBlock(self,block):
        if self.is_valid():
            lastHash = self.lastHash()
            if block.prevHash() == lastHash:
                pass
                if block.is_valid(self.difficulty):
                    print("\n")
                    print("=" * 100)
                    print("Block is valid, adding it to the blockchain")
                    self.blockchain.append((block,datetime.now(),self.difficulty))
                    try:
                        timeToMine = self.blockchain[-1][1] - self.blockchain[-2][1]
                        print(f"Time to mine the block: {timeToMine.seconds} s")
                        if timeToMine > timedelta(seconds=12):
                            self.difficulty -= 1
                            print(f"The difficulty has been decreased to {self.difficulty}")
                        elif timeToMine < timedelta(seconds=8):
                            self.difficulty += 1
                            print(f"The difficulty has been increased to {self.difficulty}")
                    except IndexError as e:
                        pass
                    print("=" * 100)
                
    
    '''
    Check if the block chain is valid.
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
    
    '''
    Return the block to mine
    '''
    def getBlockToMine(self):
        return self.lastHash() + bytearray(os.urandom(1000-36 - 32))
            
    '''
    Return the last block of the blockchain
    '''
    def lastBlock(self):
        return self.blockchain[-1]
    
    '''
    Return the last hash of the blockchain
    '''
    def lastHash(self):
        if len(self.blockchain) == 0:
            return self.initHash
        return self.lastBlock()[0].hash()
    
    '''
    Display the blockchain informations
    '''
    def __str__(self):
        string = f"The blockchain is {len(self.blockchain)} blocks long\n"
        for i,b in enumerate(self.blockchain):
            
            string += f"Block {i}"
            if i == 0:
                string += " (genesis block)"
            else:
                string += f" time to mine: {(b[1] - self.blockchain[i-1][1]).seconds} s (difficulty {b[2]})"
            string += f"\n{b[0]}\n"
        
        return string

'''
Mine a block with the given difficulty
'''
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
    try:
        for i in range(100):
            
            nextBlock = bc.getBlockToMine()
            blockSolution = mine(nextBlock,bc.difficulty)
            blockBytes = bytearray(nextBlock + blockSolution + bytearray(sha256(nextBlock+blockSolution).digest()))
            bc.submitBlock(Block(blockBytes))
    except KeyboardInterrupt:
        pass
    
    print(bc)
    
    