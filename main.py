from register import Register
from order import Order
from blockchain import Blockchain
import time
import qrcode

print("Welcome to SUPPLY CHAIN MANAGEMENT\n\n")
print("Few instructions and assumptions made:\n")
print("Products pid=[1,2,3,4,5,6,7,8,9,10,11,12] are manufactured by the manufacturer")
print("Manufacturer automatically dispatches item to distributor while chosing 5: Send item")
print("A block contains 3 transactions. Merkle tree is constructed by constinuously hashing t1,t2,t3")
print("We have simulated DPoS near to perfection. The users vote randomly to one another")
print("The user with maximum stake pool will be elected as the block producer and rewards will be distributed proportionately")
print("\n")

reg=Register()
ord= Order()
blk=Blockchain()
orderCnt=5001
blk.initiategenesisblock(time.time())


while True:
    print(
       """ 
Select any one of the following : 
    1 : Register
    2 : Add block onto blockchain 
    3 : View blockchain / transactions
    4 : Buy a product (Client Request) 
    5 : Deliver item (dist -> client)
    6 : View Product Status (QR Code)
    7 : View Pending orders
    8 : Resolve Conflict (Client/Distributor Complaining about delivery of products)  
    9 : View profile
    0 : Exit

"""
)
    choice = input("Enter your choice: ")
    if choice=='0':
        print("\nProject Done by Group 15:\nSuman Sekhar Sahoo (2021A7PS2605H)")      
        break

    elif choice=='1':
        print("\nREGISTER\n")
        while True:
            print("C: Client\nD: Distributor\nM: Manufacturer\nNOTE: There can be only 1 manufacturer\n")
            utype= input("Enter user type (C/D/M): ")
            if utype.upper()=='C':
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

            elif utype.upper()=='D':
                x=int(input("Enter user_id: "))
                if reg.checkId(x) ==-1:
                    print("User already exists")
                else:
                    y=int(input("Enter amount (min 50 for registering) Your stake will be amount-50 : "))
                    if y>=50:
                        reg.addDistb(x,y-50)
                    else:
                        print("Insufficient amount to register")
            
            elif utype.upper()=='M':
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
            ag=input("\nRegister more users? (Y/N):")
            if ag.upper()=='N':
                break
            elif ag.upper()=='Y':
                continue
            else:
                print("Invalid choice!")
                break

    elif choice=='2':
        print("\nADD A BLOCK INTO BLOCKCHAIN\n")
        if len(blk.pendingTranac)<3:
            print("Minimum 3 Pending transactions required to start adding block to Blockchain")
        else:
            blkproducer,stakeWeights=blk.delegatedProofOfStake(reg.userId,reg.stakes)
            totalBlockReward=0
            noOfBlocks=len(blk.pendingTranac)//3
            for i in range(len(blk.pendingTranac)//3):
                blk.addblock(time.time(),blkproducer)
                totalBlockReward+=50
            print(f"Total reward to produce {noOfBlocks} blocks is {totalBlockReward}")
            print("The reward will be distributed to the userIDs that elected the blockproducer in proportion of their stake in the pool\n")
            for i in stakeWeights:
                reg.stakes[i]+=totalBlockReward*stakeWeights[i]
                print(f"userID {i} rewarded with amt: {totalBlockReward*stakeWeights[i]}")

    elif choice=='3':
        print("\nVIEW BLOCKCHIAN / TRANSACTIONS\n")
        print("1: View Blockchain (Prints Block Headers)\n2: View verified Transactions (Prints transactions added to the blockchain)\n3: View unverified transactions (Prints transactions that are yet to be added onto blockchain)")
        ch=input("Enter choice: ")
        if ch=='1':
            for i in blk.chain:
                blk.printBlock(i)
        elif ch=='2':
            if len(blk.verifiedTransac)==0:
                print("No transactions verified and added to blockchain yet!")
            else:
                for i in blk.verifiedTransac:
                    print("\n{")
                    for j in i:
                        print(j)
                    print("}\n")
        elif ch=='3':
            if len(blk.pendingTranac)==0:
                print("No unverified transactions yet")
            else:
                for i in blk.pendingTranac:
                    print("\n{")
                    for j in i:
                        print(j)
                    print("}\n")
            
        else:
            print("Invalid choice!")

    elif choice=='4':
        if len(reg.manufId)==0:
            print("No manufacturer registered yet! Can't buy any product")
        else:
            if len(reg.distbId)==0:
                print("No distributors registered yet! Can't deliver products")
            else:
                print("\nBUY A PRODUCT (FOR CLIENTS)\n")
                buyer_id= int(input("Enter ClientID: "))
                if buyer_id not in reg.consumerId:
                    print("ClientID not found!")
                else:
                    print("Products pid=[1,2,3,4,5,6,7,8,9,10,11,12] are manufactured by the manufacturer")
                    prid= int(input("Enter product ID: "))
                    if prid not in range(1,13):
                        print("Product not found!")
                    else:
                        avDistb=[]
                        for i in reg.distbId:
                            if i not in ord.distbBusy:
                                avDistb.append(i)
                        if len(avDistb)==0:
                            print("Sorry no distributors currently available!")
                        else:
                            print("List of all Distributors available (Not Busy delivering any other order): ")
                            for i in avDistb:
                                print(i)

                            db=int(input("Enter distbID: "))
                            if db not in avDistb:
                                print("Distb not availlable")
                            else:
                                otime= time.time()
                                ord.newOrder(buyer_id,prid,db,otime,orderCnt)
                                print(f"OrderID: {orderCnt} sucessfully placed with DistributorID {db}")
                                orderCnt+=1

    elif choice=='5':
        if len(reg.manufId)==0:
            print("No manufacturer registered yet!")
        else:
            if len(reg.distbId)==0:
                print("No distributor registered yet!")
            else:
                print("\nDELIVER A PRODUCT (FOR DISTRIBUTORS)\n")
                ord.printIncompleteOrders()
                did=int(input("Enter distributer ID: "))
                if did not in ord.distbBusy:
                    print("No pending orders to be delivered by you")
                else:
                    odid=ord.distbBusy[did]
                    print(f"You have a pending order orderID {odid} of ProductID:{ord.orders[odid][1]} for clientID {ord.orders[ord.distbBusy[did]][0]}")
                    conf=input("Deliver the product? (Y/N): ")
                    if conf.upper()=='Y':
                        ord.orderDelivered(odid,did,reg.manufId[0],time.time())
                        transaction=[]
                        transaction.append(f"DistributorID {did} received product from ManufacturerID {reg.manufId[0]} at {ord.shipped[odid][2]}")
                        transaction.append(f"DistributorID {did} dispatched at {ord.shipped[odid][2]}")
                        transaction.append(f"ClientID received product at {ord.shipped[odid][2]}")
                        blk.pendingTranac.append(transaction)
                        print(f"Order (orderID: {odid}) successfully delivered to clientID {ord.orders[odid][0]}")
                    elif conf.upper()=='N':
                        print("Order still pending to be delivered by you! You cannot undertake any other orders until this ordered is delivered!")
                        
                            
    elif choice=='6':
        if len(ord.orders)==0:
            print("No orders placed yet!")
        else:
            print("\nVIEW PRODUCT STATUS (QR CODE)\n")
            ord.printAllOrders()
            oid= int(input("Enter OrderID: "))
            if oid not in ord.orders:
                print("OrderID not found!")
            else:
                if ord.orders[oid][4]==False:
                    order_status_msg=f"""
OrderID: {oid}\n
ClientID {ord.orders[oid][0]} ordered ProductID pid: {ord.orders[oid][1]} at {time.ctime(ord.orders[oid][3])}\n
Order was placed with DistributorID: {ord.orders[oid][2]}\n
Product not yet delivered by Distributor
"""
                    img=qrcode.make(order_status_msg)
                    img.save(f"qr{oid}.png")
                    print(f"QR generated with filename: qr{oid}.png")
                else:
                    order_status_msg=f"""
OrderID: {oid}\n
ClientID {ord.orders[oid][0]} ordered ProductID pid: {ord.orders[oid][1]} at {time.ctime(ord.orders[oid][3])}\n
ManufacturerID {reg.manufId[0]} sent product to DistributorID {ord.shipped[oid][0]} at {time.ctime(ord.shipped[oid][2])}\n
Distributor {ord.shipped[oid][0]} delivered product to ClientID {ord.orders[oid][0]} at {time.ctime(ord.shipped[oid][2])}
"""
                    img=qrcode.make(order_status_msg)
                    img.save(f"qr{oid}.png")
                    print(f"QR generated with filename: qr{oid}.png")

    elif choice=='7':
        if len(ord.distbBusy)==0:
            print("No pending orders to be delivered!")
        else:
            print("\nVIEW PENDING DELIVERY LIST\n")
            ord.printIncompleteOrders()

    elif choice=='8':
        print("COMPLAINT PORTAL\n")
        cid=int(input("Enter ClientID: "))
        if cid not in reg.consumerId:
            print("ClientID not found!")
        else:
            print("List of orders placed by you:")
            corders=[]
            for i in ord.orders:
                if ord.orders[i][0]==cid:
                    corders.append(i)
                    print(f"OrderID: {i} placed with DistributorID: {ord.orders[i][2]}")
            if len(corders)==0:
                print("No orders placed by you!")
            else:
                ordid=int(input("Enter OrderID from the above list: "))
                if ordid not in corders:
                    print("Invalid orderID")
                else:
                    print(f"Your Complaint: OrderID {ordid} not deliverd yet by DistributorID {ord.orders[ordid][2]}")
                    distbcomp=input(f"DistributorID {ord.orders[ordid][2]}, do you claim to have delivered the product? (Y/N): ")
                    if distbcomp.upper()=='N':
                        print("Distributor agrees that he didn't deliver the product")
                    elif distbcomp.upper()=='Y':
                        print("Distributor claims he has delivered the product\n\n")
                        if ord.orders[ordid][4]==True:
                            print("THE LIAR IS: Client")
                            reg.stakes[cid]-=50
                            print("You have been penalized! Your stakes has been deducted by 50")
                            print(f"Updated stake of ClientID: {cid}= {reg.stakes[cid]}\n")
                            if reg.stakes[cid]<50:
                                reg.consumerId.remove(cid)
                                reg.userId.remove(cid)
                                del reg.stakes[cid]
                                print("Since your updated stake balance < 50, you have been kicked out of the Blockchain system!")
                        
                        else:
                            print("THE LIAR IS: Distributor")
                            reg.stakes[ord.orders[ordid][2]]-=50
                            print("You have been penalized! Your stakes has been deducted by 50")
                            if reg.stakes[ord.orders[ordid][2]]<50:
                                reg.distbId.remove(ord.orders[ordid][2])
                                reg.userId.remove(ord.orders[ordid][2])
                                del reg.stakes[ord.orders[ordid][2]]
                                print("Since your updated stake balance < 50, you have been kicked out of the Blockchain system!")

    elif choice=='9':
        if len(reg.userId)==0:
            print("No users registered yet!")
        else:
            print("\nVIEW PROFILE\n")
            uid=int(input("Enter UserID: "))
            if uid not in reg.userId:
                print("UserID does not exixts!")
            else:
                if uid in reg.consumerId:
                    print("User Type: CLIENT")
                    print("Orders placed:",end=" ")
                    for i in ord.orders:
                        if ord.orders[i][0]==uid:
                            print(i,end=", ")
                    print(" ")

                elif uid in reg.distbId:
                    print("User Type: DISTRIBUTOR")
                    print("Orders delivered (OrderID):",end=" ")
                    for i in ord.shipped:
                        if ord.shipped[i][0]==uid:
                            print(i,end=", ")
                    print(" ")
                    for i in ord.orders:
                        if ord.orders[i][2]==uid and ord.orders[i][4]==False:
                            print(f"Pending Order (OrderID): {i}")
                else:
                    print("User Type: MANUFACTURER")
                print(f"Stake: {reg.stakes[uid]}")

    else:
        print("Invalid Choice!")
