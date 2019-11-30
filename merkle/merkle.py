import math
import hashlib

class MerkleTree:

    def __init__(self, transactions):
        if len(transactions) == 0:
            self.root = None
        else:
            self.transactions = list(transactions)
            length = len(transactions)
            for i in range(length,2**(math.ceil(math.log2(length)))):
                self.transactions.append(transactions[-1])

            self.root = self.buildTree(0,len(self.transactions)-1)
    
    def buildTree(self,start,end):
        if(start == end):
            # return 1
            return hashlib.sha256(str(self.transactions[start]).encode()).hexdigest()
        tree = []
        mid = (start+end)//2
        tree.append(self.buildTree(start,mid))
        tree.append(self.buildTree(mid+1,end))
        return hashlib.sha256(str(tree).encode()).hexdigest()
        # return 2

    def get_root(self):
        return self.root
