# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:21:08 2019

@author: tmedeiros
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt


# Inicializacao de parametros

def transforma_polar(x, y, theta):
    delta_x = xref - x
    delta_y = yref - y

    rho = m.sqrt(m.pow(delta_x, 2) + m.pow(yref - delta_y, 2))
    alpha = m.atan2(delta_y, delta_x) - theta
    beta = - theta - alpha

    return rho, alpha, beta


pi = m.pi
xi = 0
yi = 0
thetai = -pi/2
xref = 0
yref = 0
xg = 150
yg = 0
theta_ref = pi/2
Krho = 3
Kalpha = 8
Kbeta = -3
dt = 0.01  # Passo de integracao
tf = 50

t = np.linspace(0, tf, num=tf/dt + 1)

x = []
y = []
x.append(xi)
y.append(yi)
theta = thetai

x_lini = xi - xg
y_lini = yi - yg
rho, alpha, beta = transforma_polar(x_lini, y_lini, theta)
beta = beta + theta_ref

for ta in t:

    v = Krho * rho
    d_theta = Kalpha * alpha + Kbeta * beta

    if d_theta > 10:
        d_theta = 10

    if v > 2:
        v = 2

    # Calculo do modelo cinematico do robo
    vx = v * m.cos(theta)
    vy = v * m.sin(theta)
    theta = theta + dt * d_theta

    xa = x[len(x) - 1] + dt * vx
    ya = y[len(y) - 1] + dt * vy

    x.append(xa)
    y.append(ya)

    xlin = xa - xg
    ylin = ya - yg
    # Transformando para polar
    rho, alpha, beta = transforma_polar(xlin, ylin, theta)
    beta += theta_ref

plt.plot(x, y)
plt.show()
plt.xlabel('x(m)')
plt.ylabel('y(m)')