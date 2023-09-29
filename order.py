class Order:
    def __init__(self):
        self.orders={}
        self.shipped={}

    def newOrder(self,user_id,pid,otime,order_id):
        self.orders[order_id]=[user_id,pid,otime,False]

    def orderDelivered(self,order_id,distid,manid,dtime):
        self.orders[order_id][3]=True
        self.shipped[order_id]=[distid,manid,dtime]

    def printIncompleteOrders(self):
        print("List of incomplete orders: ")
        for i in self.orders:
            if self.orders[i][3]==False:
                print(i)
        print("\n")

    def printAllOrders(self):
        print("List of all orders: ")
        for i in self.orders:
            print(i)
        print("\n")

