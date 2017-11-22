import sys, pygame, os
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pygame.locals import *
import random

#pygame.init()



pygame.display.set_caption("Fitt's law experiment - Ramkiran_Chevendra")

ncircles = int(sys.argv[1])
#bradius = int(sys.argv[2])
#tradius = int(sys.argv[3])


bradius = [223,216,170]
tradius = [20,27]
'''
for i in range(0,3):
    a = random.randint(150, 230)
    if a not in bradius:
        bradius.append(a)
    else:
        a = random.randint(150, 230)
        bradius.append(a)
for j in range(0,2):
    b = random.randint(15,30)
    if b not in tradius:
        tradius.append(b)
    else:
        b = random.randint(15,30)
        tradius.append(b)
print(bradius)
print(tradius)
'''
FPS = 200
done = False

FPSCLOCK = pygame.time.Clock()
#DISPLAYSURF = pygame.display.set_mode((700,520))
#pygame.display.set_caption("Fitt's law experiment - Ramkiran_Chevendra")


n = 360/ncircles

list = []
ID1 = []
MT1 = []


count = 1

def calculate_parameters(n_circles, bigradius, targetradius, vtime, count):
    time_btw_clicks = []

    g = (bigradius/targetradius)+1

    ID1.append(math.log(g,2))

#print(ID)

    print(vtime)

    if(len(vtime)>1):
        for i in range(1,n_circles):
            a = int(vtime[i]) - int(vtime[i-1])
            if(i%2 == 1):
                time_btw_clicks.append(a)
            else:
                continue


    print(time_btw_clicks)
    MT1.append(sum(time_btw_clicks)/(1000*len(time_btw_clicks)))


    print(ID1)
    print(MT1)

    reg = pd.DataFrame(columns = ['ncircles', 'bradius', 'tradius', 'ID', 'MT'])

    reg.set_value(count,'ncircles',ncircles)
    reg.set_value(count,'bradius', bigradius)
    reg.set_value(count,'tradius', targetradius)
    reg.set_value(count,'ID', ID1[count-1])
    reg.set_value(count,'MT', MT1[count-1])

    reg['IDMT'] = ID1[count-1] * MT1[count-1]
    reg['IDsquare'] = ID1[count-1] * ID1[count-1]
    reg['MTsquare'] = MT1[count-1] * MT1[count-1]
    reg['Throughput'] = ID1[count-1]/MT1[count-1]


    print(reg)

    if(os.path.isfile("C:/School/Assignments/CS 522/Assignment3/Project/Data.csv") == True):
        with open("C:/School/Assignments/CS 522/Assignment3/Project/Data.csv",'a') as f:
            reg.to_csv(f,index=False, header=False)
    else:
        reg.to_csv("C:/School/Assignments/CS 522/Assignment3/Project/Data.csv", index=False)

def graph(formula, x_range):
    u = np.array(x_range)
    v = eval(formula)
    plt.plot(u, v)
    png_name3 = "C:/School/Assignments/CS 522/Assignment3/Project/Regression_equation.png"
    plt.savefig(png_name3, dpi=120)


for k in range(0,len(bradius)):
    for l in range(0, len(tradius)):
        pygame.init()
        DISPLAYSURF = pygame.display.set_mode((1024, 800))
        DISPLAYSURF.fill((255, 255, 255))
        points = []
        time = []

        for i in range(0,ncircles):
            x = int(400 + (bradius[k] * math.cos(n + (i*(2/ncircles)*math.pi))))
            y = int(300 + (bradius[k] * math.sin(n + (i*(2/ncircles)*math.pi))))
            list.append([x,y])
            x = 0
            y = 0

        for j in range(0, ncircles):
            if(int(j%2) == 0):
                pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (list[j][0], list[j][1]), tradius[l],1)
            else:
                pygame.draw.circle(DISPLAYSURF, (255, 0, 0), (list[j][0], list[j][1]), tradius[l],1)

            pygame.display.flip()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == MOUSEBUTTONDOWN:
                    points.append(event.pos)
                    time.append(pygame.time.get_ticks())

            if (len(points)>1):
                pygame.draw.lines(DISPLAYSURF, (0,0,0), False, points, 1)
                pygame.display.update()

                pygame.display.flip()
            if len(points)== ncircles:
                calculate_parameters(ncircles, bradius[k], tradius[l], time, count)
                count = count + 1
                break


reg1 = pd.read_csv("C:/School/Assignments/CS 522/Assignment3/Project/Data.csv")

if(len(reg1.index)>6 or len(reg1.index)<6):
    pygame.quit()
else:
    ID_list = reg1['ID']
    MT_list = reg1['MT']
    IDMT_list = reg1['IDMT']
    IDsquare_list = reg1['IDsquare']
    MTsquare_list = reg1['MTsquare']

    sum_ID = sum(ID_list)
    sum_MT = sum(MT_list)
    sum_IDMT = sum(IDMT_list)
    sum_IDsquare = sum(IDsquare_list)
    sum_MTsquare = sum(MTsquare_list)
    sum_ID_square = sum_ID * sum_ID

    a = ((sum_MT * sum_IDsquare) - (sum_ID * sum_IDMT))/((6 * sum_IDsquare) - sum_ID_square)
    print(a)
    b = ((6 * sum_IDMT) - (sum_ID * sum_MT)) / ((6 * sum_IDsquare) - sum_ID_square)
    print(b)

    print("The regression coefficients are a = {} and b = {} respectively".format(a,b))
    #x = reg1['ID']
    #y = reg1['MT']
    plt.plot(reg1['ID'], reg1['MT'])
    plt.axis([2.8,3.8,1.2,1.5])
    #plt.quiver(x[:-1],y[:-1],x[1:]-x[:-1],y[1:]-y[:-1])
    plt.title('Index of Difficulty Vs Movement Time')
    plt.xlabel('Index of Difficulty')
    plt.ylabel('Movement time in seconds')

    png_name1 = "C:/School/Assignments/CS 522/Assignment3/Project/IDMT.png"
    plt.savefig(png_name1, dpi = 120)
    graph("{} + {}*u".format(a, b), range(1, 5))
    plt.close()

    plt.plot(reg1['ID'], reg1['Throughput'])
    plt.title('Index of Difficulty Vs Throughput')
    plt.xlabel('Index of Difficulty')
    plt.ylabel('Throughput')

    png_name2 = "C:/School/Assignments/CS 522/Assignment3/Project/IDThroughput.png"
    plt.savefig(png_name2, dpi = 120)


pygame.quit()





