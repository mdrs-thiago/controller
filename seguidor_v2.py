# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:01:27 2019

@author: tmedeiros
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt
#Inicializacao de parametros

xi = 0
yi = 0
thetai = 3*m.pi/4
v = 1      #Velocidade constante para este problema.
Kv = 1
Kw = 3
a = 2 
b = 5
c = 2
linha = [a, b, c]
graph_x = np.linspace(-20,100,num=1000)
graph_y = (a*graph_x + c)/(-b)
#Criacao dos passos necessarios para o controle
dt = 0.05 #Passo de integracao
tf = 50
t = np.linspace(0,tf,num=tf/dt +1)


#Objetivo de armazenar os dados para observacao grafica
x = []
y = []
x.append(xi)
y.append(yi)
theta = thetai

for ta in t:
    posAtual = [x[len(x)-1],y[len(y)-1],1]
    distLin = np.dot(linha,posAtual)/m.sqrt(m.pow(linha[0],2) + m.pow(linha[1],2))
    
    theta_erro = m.atan2(-linha[0],linha[1])
    d_theta = Kw*(theta_erro - theta)
    d_theta = d_theta - Kv*distLin
    
    #Modelo cinematico do robo  
    vx = v*m.cos(theta)
    vy = v*m.sin(theta)
    theta = theta + dt*d_theta
  
    #Integra a velocidade para obter as estimativas de posicao
    xa = x[len(x)-1] + dt*vx
    ya = y[len(y)-1] + dt*vy
    
    x.append(xa)
    y.append(ya)
    
plt.plot(x,y)
plt.plot(graph_x,graph_y)
plt.xlabel('x(m)')
plt.ylabel('y(m)')