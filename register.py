class Register:
    def __init__(self):
        self.userId=[]     #stores list of all registered users
        self.distbId=[]    #stores list of all registered distributors
        self.consumerId=[] #stores list of all registered Clients
        self.manufId=[]    #contains list (only 1 element allowed) of manufacturer. The one member condition is checked in main.py
        self.stakes={}     #a dictionary contains userId as key and their stake as value

    #function used to check if a userId is registered
    def checkId(self,user_id):
        if user_id in self.userId:
            return -1
        else:
            return 1
    #function initializes a client with appropriate values
    def addConsumer(self,user_id,stake):
        self.userId.append(user_id)
        self.consumerId.append(user_id)
        self.stakes[user_id]=stake
        print("Consumer successfully registered!\n")

    #function initializes a manufacturer with appropriate values
    def addManuf(self,user_id,stake):
        self.userId.append(user_id)
        self.manufId.append(user_id)
        self.stakes[user_id]=stake
        print("Manufacturer successfully registered!\n")

    #function initializes a distributor with appropriate values
    def addDistb(self,user_id,stake):
        self.userId.append(user_id)
        self.distbId.append(user_id)
        self.stakes[user_id]=stake
        print("Distributor successfully registered!\n")


