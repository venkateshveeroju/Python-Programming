#Input=[1,'A',5,'B',10,'A',8,'A',17,'B',17]
#Input=[100,'C',100,'C',115,'C',119,'C',121,'C',144,'C',154,'C',157,'G',158,'C',171,'C',179,'C',194,'C',206,'C',214,'C',227,'C',229,'C',231,'C',298]
#Input=[1,'nepper',15,'hamster',24,'philipp',30,'mmautne',31,'hamster',49,'hamster',55,'thebenil',57,'fliegimandi',59,'ev',61,'philipp',64,'philipp',65,'ev',74,'philipp',69,'philipp',71,'fliegimandi',78,'hamster',78,'mio',95,'hamster',103,'macquereauxpl',135]
# read_input=input("Please enter input  ")
# Input = [x for x in read_input.split()]
Input=[100,'A',100,'A',115,'A',119,'A',144,'A',145,'A',157,'A',158,'A',171,'A',179,'A',194,'A',206,'A',207,'A',227,'A',229,'A',231,'A',234100,'A',100,'A',115,'A',119,'A',144,'A',145,'A',157,'A',158,'A',171,'A',179,'A',194,'A',206,'A',207,'A',227,'A',229,'A',231,'A',234]
name=[]
bid=[]
i=0
tempBid=[]
temp=[]
length=len(Input)/2
for k in range(int(length)):
    name.append(Input[2*i+1])
    bid.append(Input[2*i+2])
    i+=1

########################
CurrentPrice=Input[0]
latest=bid[1]
CurrentBid=bid[0]
t=0
s=[]
ss=1
temp.append(Input[0])

temp.append(bid[t])
tempBid.append(Input[0])
for l in range (len(bid)-1):
    temp.append( bid[t+1])
    if((temp[t+1]<temp[t+2])& (temp[t+1]>tempBid[t])):
        if(ss == 1):
            print(temp[t+1],tempBid[t])
            ss+=1
        tempBid.append(temp[t+1]+1)
        print(temp[t+2],tempBid[t+1])
        t+=1
    elif((temp[t+1]<temp[t+2] )& (temp[t+1]<=tempBid[t])):
        s = temp[:]
        s.sort()
        tempBid.append(sorted(s)[-2] + 1)
        print(temp[t + 2], tempBid[t + 1])
        t += 1
    elif(temp[t+1]>temp[t+2]):
        if (ss == 1):
            print(temp[t + 1], tempBid[t])
            ss += 1
        s = temp[:]
        s.sort()
        tempBid.append(sorted(s)[-2] + 1)
        print(temp[t +2], tempBid[t+1])
        t += 1
    elif (temp[t + 1] == temp[t + 2]):
        if (ss == 1):
            print(temp[t + 1], tempBid[t])
            ss += 1

        if (temp[t + 2]==max(temp)):
            tempBid.append(temp[t + 2])
            print(temp[t + 2], tempBid[t + 1])
            t += 1
        else:
            s = temp[:]
            s.sort()
            tempBid.append(sorted(s)[-2] + 1)
            print(temp[t + 2], tempBid[t + 1])
            t += 1
    else:
        tempBid.append(tempBid[t])
        print(temp[t+2],tempBid[t+1])
        t +=1
a=tempBid
a.sort()
print (str(name[bid.index(max(bid))])+','+str(int(sorted(a)[-1])))

