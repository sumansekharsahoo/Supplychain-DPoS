# Supply Chain Management System – Blockchain Technology

The project aims at solving problems in Supply Chain with the help of Blockchain technology. Consensus algorithm used: Delegated Proof of Stake (DPoS)

## Group 15

- [Suman Sekhar Sahoo](https://www.github.com/sumansekharsahoo) (2021A7PS2605H)
- Yash Pandey (2021A8PS3194H)
- Anmol Agarwal (2021A4PS3068H)
- Sharan K (2021A8PS1537H)

## Technology Used:

Python

## Installation

This project uses the Python package **[qrcode](https://pypi.org/project/qrcode/)** to generate QR Codes for viewing product status

```
  pip install qrcode
```

## Working of the Blockchain

A block is made out of 3 Transactions. It is mined (produced in case of DPoS) by a Block Producer that is elected by a voting mechanism (discussed below).

A Block Header contains:

- Index
- Merkle Root
- Time stamp
- Previous hash
- Blockproducer Signature
- Hash

A transaction is of form:

```
{
    Distributor (Di) got from the manufacturer -> Timestamp 1
    Distributor dispatched ->Timestamp 2
    Client (Ci) received -> Timestamp 3
}
```

## DPoS Algorithm

(Implemented as a function in blockchain.py file)

```python
def delegatedProofOfStake(self,userlist,stakes):
        print("Electing the block producer...\n")
        votedFor={}

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
```

We have nearly immitated the DPoS Algorithm by implementing random voting. Each user randomly votes for some user. The weight of his vote is given by the stakes he owns. The user that has received maximum stakes as vote is elected as the Block Producer. The reward for producing a block (50) is then distributed among the user that voted in favor of the Block producer. Distribution is done in proportion of the stake they pooled.

The function here returns the BlockProducer ID and the proportion of stake the voter (of BlockProducer) pooled. These values are used in main.py to update stakes of the users.

## Description of each module

### register.py

used to store user information (ID, stakes)

- **userId**: stores list of all users
- **distbId**: stores list of all distributors
- **consumerId**: stores list of all Clients
- **manufId**: contains list (only 1 element allowed) of manufacturer
- **stakes**: a dictionary contains userId as key and their stake as valuse
- **checkId()**: function used to check if a userId is registered
- **addConsumer()**: function initializes a client with appropriate values
- **addDistb()**: function initializes a distributor with appropriate values
- **addManuf()**: function initializes a manufacturer with appropriate values

### order.py

used to store information regarding orders

- **orders**: a dictionary with key: orderID, value: array(clientID, productID, DistributorID, orderPlacedTimestamp, isDelivered), isDelivered is True if order is shipped and false otherwise
- **shipped**: a dictionary containing key: orderID, value: array(distbID,manufId, deliveryTime)
- **distbBusy**: a dictionary with key: distbId (that is currently having pending order) and value: orderID
- **newOrder()**: function that initializes orders with appropriate values and inserts the distbID to distbBusy
- **orderDelivered()**: function that updates orders array 5th element to True, removes distbID from distbBusy and initializes values in shipped array
- **printIncompleteOrders()**: prints orderID and DistbId of pending orders
- **printAllOrders()**: prints all orders (shipped and not shipped)

### blockchain.py

contains function and arrays that is used to store transactions, blockchain, create block, print block, DPoS algorithm

- **verifiedTransac**: array containing all transactions that are verified and added into blockchain
- **pendingTransac**: array containg all those transactions that are not yet added into blockchain
- **chain**: array containing Block Headers
- **merkletree()**: function that accepts first 3 transactions from pendingTransac. It first converts all the transaction into string format and calculates hashes of each transaction using **hashlib.sha256()** function and then finds hashes of t1-t2 and t3-t3 and finally calculates hash of t1-t2-t3-t3. This is called the **merkleroot**
- **initiategenesisblock()**: function that takes in timestamp as parameter and generates the Geenesis block of the blockchain and then prints it
- **addblock()**: this takes in timestamp and blockproducer as parameters. Blockproducer is calculated using delegatedProofOfStake() function and initializes the block with appropriate values and finally prints it
- **createHash()**: generates the hash value of the block by using **hashlib.sha256()** on the concatenated values of index, merkleroot, timestamp and previoushash
- **blockproducerSignature()**: generates blockproducer signature by using **hashlib.sha256()** on the concatenated string of userID (of the blockproducer) and timestamp
- **delegatedProofOfStake()**: explained above
- **printBlock()**: takes in the block dictionary as parameter and prints it in required format

### main.py

contains all the programs required to run the blockchain system on the terminal

- initializes objects of class Register(), Order(), Blockchain(), orderCount= 5001
- creates Genesis block
- Until the user exits (choice: 0), it displays the menu of actions
- contains code (in choice: 4) that would ensure that a at one time, the distributor can distribute a product to a dedicated client.
- contains code that would check for conflict (in choice: 8) and punish the LIAR by deducting amt 50 from stake. If updated stake falls below 50, the user is kicked out of the system
- contains code that would generate qrcode (choice: 6) to view the product status of required orderID
