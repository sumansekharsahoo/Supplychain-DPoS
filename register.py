class Register:
    def __init__(self):
        self.userId=[]
        self.distbId=[]
        self.consumerId=[]
        self.manufId=[]
        self.stakes={}
        # self.pidDistb={}
        # self.pidTaken=[]
        # self.productId=[1,2,3,4,5,6,7,8,9,10,11,12]

    def checkId(self,user_id):
        if user_id in self.userId:
            return -1
        else:
            return 1
    
    # def checkConsumer(self,user_id):
    #     if user_id in self.consumerId:
    #         return 1
    #     else:
    #         return -1
        
    # def checkDistb(self,user_id):
    #     if user_id in self.distbId:
    #         return 1
    #     else:
    #         return -1
    
    def addConsumer(self,user_id,stake):
        self.userId.append(user_id)
        self.consumerId.append(user_id)
        self.stakes[user_id]=stake
        print("Consumer successfully registered!\n")

    def addManuf(self,user_id,stake):
        # if len(self.manufId)>0:
        #     print("Only 1 Manufacturer allowed\n")
        self.userId.append(user_id)
        self.manufId.append(user_id)
        self.stakes[user_id]=stake
        print("Manufacturer successfully registered!\n")

    def addDistb(self,user_id,stake):
        self.userId.append(user_id)
        self.distbId.append(user_id)
        # self.pidTaken.append(pid)
        # self.pidDistb[user_id]=pid
        self.stakes[user_id]=stake
        print("Distributor successfully registered!\n")


