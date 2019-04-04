# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:26:40 2019

@author: tmedeiros
"""

#Script para controle de um sistema robótico

import numpy as np
import math as m
import matplotlib.pyplot as plt
#Inicializacao de parametros

xi = 0
yi = 0
thetai = m.pi/4
xref = -10
yref = 11
Kw = 10
Kv = 0.5
dt = 0.05 #Passo de integracao
tf = 50

t = np.linspace(0,tf,num=tf/dt +1)

x = []
y = []
x.append(xi)
y.append(yi)
theta = thetai

for ta in t:
    
    erro1 = [xref - x[len(x)-1], yref - y[len(y)-1]]
    erro = np.power(erro1,2)
    distEuc = m.sqrt(erro[0] + erro[1])
    v = Kv*distEuc

    if v > 5:
        v = 5

    theta_erro = m.atan2(erro1[1],erro1[0])
    print('theta_erro =' + str(theta_erro))

    d_theta = Kw*(theta_erro - theta)
    print('d_theta =' + str(d_theta))
      
    vx = v*m.cos(theta)
    vy = v*m.sin(theta)
    theta = theta + dt*d_theta
    print('theta =' + str(theta))
    print('---')

    xa = x[len(x)-1] + dt*vx
    ya = y[len(y)-1] + dt*vy
    
    x.append(xa)
    y.append(ya)
    
plt.plot(x,y)
plt.show()
plt.xlabel('x(m)')
plt.ylabel('y(m)')