import os
import random
import math
import numpy as np

world_size = 100
landmarks = [[20, 20],[20, 80],[80, 20],[80, 80]]

class Robot:
    def __init__(self):
        self.x = random.random()*world_size
        self.y = random.random()*world_size
        self.orient = random.random()*2*math.pi
        self.move_noise = 0.0
        self.turn_noise = 0.0
        self.sensor_noise = 0.0

    def __str__(self):
        return "x={}, y={}, z={}".format(self.x, self.y, self.orient)

    def set_pose(self, x, y, orient):
        if x<0 or x > world_size:
            raise ValueError("X value is out of range")
        if y<0 or x > world_size:
            raise ValueError("Y value is out of range")
        if orient<0 or orient > 2*math.pi:
            raise ValueError("orient value is out of range")
        self.x = x
        self.y = y
        self.orient = orient;

    def set_noise(self, move, turn, sensor):
        self.move_noise = move
        self.turn_noise = turn
        self.sensor_noise = sensor

    def move(self, turn, forward):
        self.orient += turn + random.gauss(0.0, self.turn_noise)
        self.orient %= 2*math.pi
        dis = forward + random.gauss(0.0, self.move_noise)
        dx = dis*math.cos(self.orient)
        dy = dis*math.sin(self.orient)
        self.x += dx
        self.y += dy
        self.x %= world_size
        self.y %= world_size
    
    def measurement(self):
        measure = []
        for lm in landmarks:
            dis = math.sqrt((self.x-lm[0])**2+(self.y-lm[1])**2)
            dis += random.gauss(0.0, self.sensor_noise)
            measure.append(dis)
        return measure

    def Guassian(self, x, mu, sigma):
        return math.exp(-0.5*(x-mu)**2/sigma**2)/math.sqrt(2*math.pi)*sigma

    def measure_prob(self, measure):
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Guassian(dist, self.sensor_noise, measure[i])
        return prob

if __name__ == "__main__":
    myrobot = Robot()
    myrobot.set_pose(30,50,math.pi/2)
    myrobot.set_noise(0.05, 0.05, 5.0)
    # myrobot.move(-math.pi/2, 15)
    # print(myrobot.measurement())
    # myrobot.move(-math.pi/2, 10)
    # print(myrobot.measurement())
    print(myrobot)

    N = 200
    particle=[]
    for itere in range(N):
        x = Robot()
        x.set_noise(0.05, 0.05, 5.0)
        particle.append(x)

    for itere in range(3):
        myrobot.move(0.1, 5.0)
        Z = myrobot.measurement()

        weights = []
        for rob in particle:
            rob.move(0.1, 5.0)
            weights.append(rob.measure_prob(Z))
        
        # new_partical = []
        # index = int(random.random() * N)
        # beta = 0.0
        # mw = max(weights)
        # for i in range(N):
        #     beta += random.random() * 2.0 * mw
        #     while beta > weights[index]:
        #         beta -= weights[index]
        #         index = (index + 1) % N
        #     new_partical.append(particle[index])
        # particle = new_partical
        sum_weights = sum(weights)
        cnt_weights = len(weights)
        rand_begin = random.random()/cnt_weights
        add_weight = weights[0]/sum_weights
        new_partical = []
        i = 0
        for idx in range(1, cnt_weights+1):
            thred_weights = rand_begin + float(idx-1)/cnt_weights
            while thred_weights > add_weight:
                i = (i+1)%N
                add_weight += weights[i]/sum_weights
            print("{}, {}, {}, {}, {}".format(itere, i, idx, add_weight, thred_weights))
            new_partical.append(particle[i])
        particle = new_partical
        print(len(particle))
    for rob in particle:
        print(rob)