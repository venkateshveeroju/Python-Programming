import math
read_input=input("Please input ballPosition,teamNumber,playerNumber and Playercoordinate  ")
player_info_list = [int(x) for x in read_input.split()]#loading the input values into a list
#player_info_list=store_input
x1=player_info_list[0]#X co-ordinate of ball position
y1=player_info_list[1]#Y co-ordinate of ball position
distanceCalculator=[]
distSort=[]
out_put=[]
i = 1
#Below loop calculates the distance between ball and players
for k in range((len(player_info_list)) -int(float((len(player_info_list)+1)/2))):
    try:
        xp=player_info_list[4*(i)]
        yp = player_info_list[(4 * i)+1]
        dist = math.hypot(xp - x1, yp - y1)
        distanceCalculator.append(dist)
        i+=1
        if (i>= ((len(player_info_list)/4)-2)):
            break
    except ValueError:
        print("Not a valid number.  Try again...")
distSort=distanceCalculator[:]
distSort.sort()
incrementor = 0
p=0
for j in range(len(distanceCalculator)):#loop to find the nearest player ositioned to ball
    hh= sorted(distSort)[incrementor]
    distanceIndex=distanceCalculator.index(hh)
    teamnumber = str(player_info_list[int((4 * distanceIndex ) + 2)])
    playernumber =str(player_info_list[int((4 * distanceIndex )+ 2)+1])
    out_put.append(teamnumber+' ')
    out_put.append(playernumber+' ')
    incrementor+=1
print(''.join(out_put))#display output with teamNumber,playerNumber

