from register import Register
from order import Order
import time
import qrcode

print("Welcome to SUPPLY CHAIN MANAGEMENT\n\n")
print("Few instructions and assumptions made:\n")
print("Products pid=[1,2,3,4,5,6,7,8,9,10,11,12] are manufactured by the manufacturer")
print("Manufacturer automatically dispatches item to distributor while chosing 5: Send item")

reg=Register()
ord= Order()
orderCnt=5001

while True:
    print(
       """ 
Select any one of the following : 
    1 : Add transactions
    2 : Register
    3 : Add block onto blockchain 
    4 : Buy a product (Consumer Request) 
    5 : Send item (dist -> client)
    6 : View Product Status (QR Code)
    7 : View Pending orders
    8 : Resolve Conflict (Consumer/Distributor Complaint)  
    9 : View profile
    10 : Exit

      """
      )
    choice = input("Enter your choice: ")
    if choice=='10':
        print("\nProject Done by Group 15:\nSuman Sekhar Sahoo (2021A7PS2605H)")      
        break
    elif choice=='1':
        pass
    elif choice=='2':
        print("C: Consumer\nD: Distributor\nM: Manufacturer\nNOTE: There can be only 1 manufacturer\n")
        utype= input("Enter user type (C/D/M): ")
        if utype=='C':
            x=int(input("Enter user_id: "))
            if reg.checkId(x) ==-1:
                print("User already exists")
            else:
                y=int(input("Enter amount (min 50 for registering) Your stake will be amount-50 : "))
                if y>=50:
                    reg.addConsumer(x,y-50)
                    # print(*reg.consumerId)
                else:
                    print("Insufficient amount to register")

        elif utype=='D':
            x=int(input("Enter user_id: "))
            if reg.checkId(x) ==-1:
                print("User already exists")
            else:
                y=int(input("Enter amount (min 50 for registering) Your stake will be amount-50 : "))
                if y>=50:
                    reg.addDistb(x,y-50)
                else:
                    print("Insufficient amount to register")
        
        elif utype=='M':
            x=int(input("Enter user_id: "))
            if len(reg.manufId)>0:
                print("Manufacturer already exists")
            else:
                if reg.checkId(x) ==-1:
                    print("User already exists")
                else:
                    y=int(input("Enter amount (The whole amount will be your stake): "))
                    reg.addManuf(x,y)
        else:
            print("Invalid User Type")

    elif choice=='3':
        pass

    elif choice=='4':
        if len(reg.manufId)==0:
            print("No manufacturer registered yet! Can't buy any product")
        else:
            if len(reg.distbId)==0:
                print("No distributors registered yet! Can't deliver products")
            else:
                buyer_id= int(input("Enter ConsumerId: "))
                if buyer_id not in reg.consumerId:
                    print("ConsumerId not found!")
                else:
                    print("Products pid=[1,2,3,4,5,6,7,8,9,10,11,12] are manufactured by the manufacturer")
                    prid= int(input("Enter product ID: "))
                    if prid not in range(1,13):
                        print("Product not found!")
                    else:
                        otime= time.time()
                        ord.newOrder(buyer_id,prid,otime,orderCnt)
                        print(f"Order orderId: {orderCnt} sucessfully placed")
                        orderCnt+=1

    elif choice=='5':
        if len(reg.manufId)==0:
            print("No manufacturer registered yet!")
        else:
            if len(reg.distbId)==0:
                print("No distributor registered yet!")
            else:
                ord.printIncompleteOrders()
                did=int(input("Enter distributer ID: "))
                if did not in reg.distbId:
                    print("Distributer not found!")
                else:
                    oid=int(input("Enter OrderID that you want to deliver: "))
                    if oid not in ord.orders:
                        print("OrderID not found!")
                    else:
                        ord.orderDelivered(oid,did,reg.manufId[0],time.time())
                        print(f"OrderId {oid} of Product pid: {ord.orders[oid][1]} delivered to consumerId: {ord.orders[oid][0]} by Distributor Id: {did}")
                        
                            
            
    elif choice=='6':
        if len(ord.orders)==0:
            print("No orders placed yet!")
        else:

            ord.printAllOrders()
            oid= int(input("Enter order ID: "))
            if oid not in ord.orders:
                print("OrderID not found!")
            else:
                if ord.orders[oid][3]==False:
                    order_status_msg=f"""
OrderID: {oid}

ConsumerId {ord.orders[oid][0]} ordered ProductID pid: {ord.orders[oid][1]} at {time.ctime(ord.orders[oid][2])}

Product not yet dispatched by manufacturer

"""
                    img=qrcode.make(order_status_msg)
                    img.save(f"qr{oid}.png")
                    print(f"QR generated with filename: qr{oid}.png")
                else:
                    order_status_msg=f"""
OrderID: {oid}

ConsumerID {ord.orders[oid][0]} ordered ProductID pid: {ord.orders[oid][1]} at {time.ctime(ord.orders[oid][2])}

ManufacturerID {reg.manufId[0]} sent product to DistributorID {ord.shipped[oid][0]} at {time.ctime(ord.shipped[oid][2])}

Distributor {ord.shipped[oid][0]} delivered product to consumer {ord.orders[oid][0]} at {time.ctime(ord.shipped[oid][2])}

"""
                    img=qrcode.make(order_status_msg)
                    img.save(f"qr{oid}.png")
                    print(f"QR generated with filename: qr{oid}.png")

    elif choice=='8':
        x=int(input("Enter consumerID: "))
        if x not in reg.consumerId:
            print("UserID not found")
        else:
            ord.printAllOrders()
            o=int(input("Enter orderID: "))
            if ord.orders[o][0]!=x:
                print("Invalid orderID")
            else:
                print("Your complaint: You didn't receive product but distributor claims to have delivered the product")
                y= int(input("Enter DistributorID (that claims to have delivered product): "))
                if y in reg.distbId:
                    print("Invalid DistributorID")
                else:
                    print("Your complaint: You claim to have deliverd the product but consumer denies delivery\n\n")
                    if ord.orders[o][3]==True and ord.shipped[0]==y:
                        reg.stakes[x]-=100
                        print("Consumer lied about not receiving the product! Consumer has been penalised (amount 100 deducted from deposit)")
                        print(f"Updated stake of consumerID {x}= {reg.stakes[x]}")
                    elif ord.orders[o][3]==False:
                        reg.stakes[y]-=100
                        print("Distributor lied about having delivered the product! Distributor has been penalised (amount 100 deducted from deposit)")
                        print(f"Updated stake of distributorID {x}= {reg.stakes[y]}")





    else:
        print("Invalid Choice!")



# reg=Register()
# x=int(input("Enter user_id:"))
# if reg.checkId(x) ==-1:
#     print("User already exists")
# else:
#     y=int(input("Enter stake (min 50): "))
#     if y>=50:
#         reg.addConsumer(x,y-50)
#         print(*reg.consumerId)
#     else:
#         print("Stake insufficient to register")
