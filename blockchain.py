from hashlib import sha256

def updatehash(*args):
    hashing_text= ""; h = sha256()
    for arg in args:
        hashing_text += str(arg)
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

# print(updatehash("hello world","hello"))
class Block():
    data = None
    hash = None
    nonce = 0
    previous_hash = "0"*64

    def __init__(self, data, number = 0):
        self.data = data
        self.number = number

    def hash(self):
        return updatehash(
            self.number, 
            self.previous_hash,
            self.data, 
            self.nonce
        )

    def __str__(self):
        return str("Block# : %s\nHash : %s\nPrevious : %s\nData : %s\nNonce : %s\n" %(
            self.number, 
            self.hash(), 
            self.previous_hash,
            self.data, 
            self.nonce
            ))


class Blockchain():
    difficulty = 4

    def __init__(self,chain=[]):
        self.chain = chain
    
    def add(self, block):
        self.chain.append(block)
        
    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0"*self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0"*self.difficulty:
                return False

        return True

def main():
    blockchain = Blockchain()
    database = ["hello world", "Hi", "Bye", "LOL"]

    num = 0
    for data in database:
        num += 1
        blockchain.mine(Block(data,num))

    for block in blockchain.chain:
        print(block)
    
    print(blockchain.isValid())

if __name__ == '__main__':
    main()