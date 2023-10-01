class Register:
    def __init__(self):
        self.userId=[]
        self.distbId=[]
        self.consumerId=[]
        self.manufId=[]
        self.stakes={}

    def checkId(self,user_id):
        if user_id in self.userId:
            return -1
        else:
            return 1
    
    def addConsumer(self,user_id,stake):
        self.userId.append(user_id)
        self.consumerId.append(user_id)
        self.stakes[user_id]=stake
        print("Consumer successfully registered!\n")

    def addManuf(self,user_id,stake):
        self.userId.append(user_id)
        self.manufId.append(user_id)
        self.stakes[user_id]=stake
        print("Manufacturer successfully registered!\n")

    def addDistb(self,user_id,stake):
        self.userId.append(user_id)
        self.distbId.append(user_id)
        self.stakes[user_id]=stake
        print("Distributor successfully registered!\n")


