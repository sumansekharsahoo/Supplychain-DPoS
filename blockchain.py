import hashlib
import random

class Blockchain:
    def __init__(self):
        self.verifiedTransac=[]
        self.pendingTranac=[] #pending to be added to blockchain
        self.chain=[]

    def merkletree(self,t1,t2,t3):
        hashed=[]
        t1_msg=""
        t2_msg=""
        t3_msg=""
        for i in range(3):
            t1_msg+=t1[i]
            t2_msg+=t2[i]
            t3_msg+=t3[i]
        hashed.append(str(hashlib.sha256(t1_msg.encode()).hexdigest()))
        hashed.append(str(hashlib.sha256(t2_msg.encode()).hexdigest()))
        hashed.append(str(hashlib.sha256(t3_msg.encode()).hexdigest()))
        hash12_msg=hashed[0]+hashed[1]
        hash12=str(hashlib.sha256(hash12_msg.encode()).hexdigest())
        hash33_msg=hashed[2]+hashed[2]
        hash33=str(hashlib.sha256(hash33_msg.encode()).hexdigest())
        hash1233_msg=hash12+hash33
        hash1233=str(hashlib.sha256(hash1233_msg.encode()).hexdigest())
        return hash1233
    
    def initiategenesisblock(self,timestmp):
        blk={
            'index': len(self.chain)+1,
            'merkleroot': '0',
            'timestamp':timestmp,
            'prevhash':'0',
            'blockproducer_signature':'0',
            'hash':'0',
        }
        self.chain.append(blk)
        blk_msg=f"""
[
    index: {blk['index']},
    merkleroot: {blk['merkleroot']},
    timestamp: {blk['timestamp']},
    prevhash: {blk['prevhash']},
    blockproducer_signature:{blk['blockproducer_signature']}
    hash: {blk['hash']}
]
"""
        print("Genesis Block:\n")
        print(blk_msg)

    def addblock(self,tstamp,blkproducer):
        merkleroot=self.merkletree(self.pendingTranac[0],self.pendingTranac[1],self.pendingTranac[2])
        blk={
            'index': len(self.chain)+1,
            'merkleroot':merkleroot,
            'timestamp':tstamp,
            'prevhash':self.chain[len(self.chain)-1]['hash'],
            'blockproducer_signature':self.blockproducerSignature(blkproducer,tstamp),
            'hash':self.createHash(len(self.chain)+1,merkleroot,tstamp,self.chain[len(self.chain)-1]['hash'])
        }
        self.chain.append(blk)
        for i in range(3):
            self.verifiedTransac.append(self.pendingTranac.pop(0))
        blk_msg=f"""
[
    index: {blk['index']},
    merkleroot: {blk['merkleroot']},
    timestamp: {blk['timestamp']},
    prevhash: {blk['prevhash']},
    blockproducer_signature:{blk['blockproducer_signature']}
    hash: {blk['hash']}
]
"""
        print("Block added: \n")
        print(blk_msg)
    
    def createHash(self,index,mkroot,timestmp,prevhash):
        msg=str(index)+str(mkroot)+str(timestmp)+str(prevhash)
        return str(hashlib.sha256(msg.encode()).hexdigest())

    def blockproducerSignature(self,uid,timestmp):
        msg=str(uid)+str(timestmp)
        return str(hashlib.sha256(msg.encode()).hexdigest())
    
    def delegatedProofOfStake(self,userlist,stakes):  
        print("Electing the block producer...\n")
        votedFor={}

        #For each userID, we are putting random vote to some userID
        for i in range(len(userlist)):
            votedFor[userlist[i]]=userlist[random.randint(0,len(userlist)-1)] 
            print(f"UserID: {userlist[i]} voted for {votedFor[userlist[i]]}")
        totalVoteStake={}
        for i in userlist:
            vs=0
            for j in votedFor:
                if votedFor[j]==i:
                    vs+=stakes[j]
            totalVoteStake[i]=vs
        maxv=-1
        winner=-1
        for i in totalVoteStake:
            if totalVoteStake[i]>maxv:
                maxv=totalVoteStake[i]
                winner=i
        
        stakeWeights={}
        for i in votedFor:
            if votedFor[i]==winner:
                stakeWeights[i]=stakes[i]/totalVoteStake[winner]

        
        print(f"UserID with highest total vote stake: {winner}. UserID: {winner} is chosen as the blockproducer\n")
        return winner, stakeWeights
        
    def printBlock(self,blk):
        blk_msg=f"""
[
    index: {blk['index']},
    merkleroot: {blk['merkleroot']},
    timestamp: {blk['timestamp']},
    prevhash: {blk['prevhash']},
    blockproducer_signature:{blk['blockproducer_signature']}
    hash: {blk['hash']}
]
"""
        print(f"\n{blk_msg}")


        


        

        
        