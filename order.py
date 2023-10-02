class Order:
    def __init__(self):
        #a dictionary with key: orderID, value: array(clientID, productID, DistributorID, orderPlacedTimestamp, isDelivered)
        # isDelivered is True if order is shipped and false otherwise
        self.orders={} 
        self.shipped={} #a dictionary containing key: orderID, value: array(distbID,manufId, deliveryTime)
        self.distbBusy={} #a dictionary with key: distbId (that is currently having pending order) and value: orderID

    #function that initializes orders with appropriate values and inserts the distbID to distbBusy
    def newOrder(self,user_id,pid,distb_id,otime,order_id):
        self.orders[order_id]=[user_id,pid,distb_id,otime,False]
        self.distbBusy[distb_id]=order_id

    #function that updates orders array 5th element to True, 
    # removes distbID from distbBusy and initializes values in shipped array
    def orderDelivered(self,order_id,distid,manid,dtime):
        self.orders[order_id][4]=True
        self.shipped[order_id]=[distid,manid,dtime]
        del self.distbBusy[distid]

    #prints orderID and DistbId of pending orders
    def printIncompleteOrders(self):
        print("List of incomplete orders: ")
        for i in self.orders:
            if self.orders[i][4]==False:
                print(f"OrderID {i} pending to be delivered by DistributorID {self.orders[i][2]}")
        print(" ")

    #prints all orders (shipped and not shipped)
    def printAllOrders(self):
        print("List of all orders: ")
        for i in self.orders:
            print(i)
        print("\n")

