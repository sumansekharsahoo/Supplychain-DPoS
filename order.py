class Order:
    def __init__(self):
        self.orders={}
        self.shipped={}
        self.distbBusy={}

    def newOrder(self,user_id,pid,distb_id,otime,order_id):
        self.orders[order_id]=[user_id,pid,distb_id,otime,False]
        self.distbBusy[distb_id]=order_id

    def orderDelivered(self,order_id,distid,manid,dtime):
        self.orders[order_id][4]=True
        self.shipped[order_id]=[distid,manid,dtime]
        del self.distbBusy[distid]

    def printIncompleteOrders(self):
        print("List of incomplete orders: ")
        for i in self.orders:
            if self.orders[i][4]==False:
                print(f"OrderID {i} pending to be delivered by DistributorID {self.orders[i][2]}")
        print(" ")

    def printAllOrders(self):
        print("List of all orders: ")
        for i in self.orders:
            print(i)
        print("\n")

