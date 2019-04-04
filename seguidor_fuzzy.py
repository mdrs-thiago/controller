# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:20:47 2019

@author: tmedeiros

Changelog: V1.1 
- Adicionadas novas regras de erroDist Far, erroTheta Very Negative e 
  erroTheta Very Positive, para otimização do controle fuzzy 
- Adicionados novos comentários para melhor compreensão do código
"""

import numpy as np
import math as m
import matplotlib.pyplot as plt
import skfuzzy.control as ctrl
import skfuzzy as fuzz


# Inicializacao de parametros fuzzy
pi = m.pi
universo_discurso_v = np.linspace(0, 2, num=1000)
universo_discurso_w = np.linspace(-pi, pi, num=1000)
universo_discurso_dist = np.linspace(0, 15, num=1000)
universo_discurso_derivate = np.linspace(-3, 3, num=1000)

# Definicao dos antecedentes
erro_dist = ctrl.Antecedent(universo_discurso_dist, 'erro_dist')

d_erro_dist = ctrl.Antecedent(universo_discurso_derivate, 'd_erro_dist')

erro_w = ctrl.Antecedent(universo_discurso_w, 'erro_w')

d_erro_w = ctrl.Antecedent(universo_discurso_derivate, 'd_erro_w')

# Definicao dos consequentes
vout = ctrl.Consequent(universo_discurso_v, 'vout')
vout.defuzzify_method = "mom"

wout = ctrl.Consequent(universo_discurso_w, 'wout')

wout.defuzzify_method = "centroid"

# Construcao do membership function do erro da distancia
erro_dist['rrc'] = fuzz.trimf(erro_dist.universe, [0, 0, 0.5])
erro_dist['rc'] = fuzz.trimf(erro_dist.universe, [0, 1, 1.5])
erro_dist['c'] = fuzz.trimf(erro_dist.universe, [0.5, 1.5, 2.5])
erro_dist['mc'] = fuzz.trimf(erro_dist.universe, [2, 3, 4])
erro_dist['m'] = fuzz.trimf(erro_dist.universe, [3, 6, 9])
erro_dist['mf'] = fuzz.trimf(erro_dist.universe, [4, 9, 12])
erro_dist['f'] = fuzz.trimf(erro_dist.universe, [9, 15, 15])
#erro_dist.view()

# Construcao do membership function da derivada do erro da distancia
d_erro_dist['n'] = fuzz.zmf(d_erro_dist.universe, -2, -0.5)
d_erro_dist['ln'] = fuzz.trimf(d_erro_dist.universe, [-1, -0.25, 0])
d_erro_dist['z'] = fuzz.trimf(d_erro_dist.universe, [-0.25, -0, 0.25])
d_erro_dist['lp'] = fuzz.trimf(d_erro_dist.universe, [0, 0.25, 1])
d_erro_dist['p'] = fuzz.smf(d_erro_dist.universe, 0.5, 2)
#d_erro_dist.view()

# Construcao do membership function do erro na velocidade angular
erro_w['vn'] = fuzz.zmf(erro_w.universe, -pi / 2, -pi / 4)
erro_w['n'] = fuzz.trimf(erro_w.universe, [-3 * pi / 4, -pi / 4, -pi / 8])
erro_w['ln'] = fuzz.trimf(erro_w.universe, [-pi / 4, -pi / 8, 0])
erro_w['z'] = fuzz.trimf(erro_w.universe, [-pi / 8, 0, pi / 8])
erro_w['lp'] = fuzz.trimf(erro_w.universe, [0, pi / 8, pi / 4])
erro_w['p'] = fuzz.trimf(erro_w.universe, [pi / 8, pi / 4, 3 * pi / 4])
erro_w['vp'] = fuzz.smf(erro_w.universe, pi / 4, pi / 2)
#erro_w.view()    

# Construcao do membership function da derivada do erro de w
#d_erro_w.automf(names=['n','ln','z','lp','p'])
d_erro_w['n'] = fuzz.zmf(d_erro_dist.universe, -2, -0.5)
d_erro_w['ln'] = fuzz.trimf(d_erro_dist.universe, [-1, -0.25, 0])
d_erro_w['z'] = fuzz.trimf(d_erro_dist.universe, [-0.25, -0, 0.25])
d_erro_w['lp'] = fuzz.trimf(d_erro_dist.universe, [0, 0.25, 1])
d_erro_w['p'] = fuzz.smf(d_erro_dist.universe, 0.5, 2)
#d_erro_w.view()

# Construcao do membership function da velocidade

vout['z'] = fuzz.trimf(vout.universe, [0, 0, 0.2])
vout['lp'] = fuzz.trimf(vout.universe, [0, 0.2, 0.4])
vout['p'] = fuzz.trimf(vout.universe, [0.2, 0.8, 1.5])
vout['vp'] = fuzz.smf(vout.universe, 0.8, 1.5)
#vout.view()

# Construcao do membership function de w
#wout.automf(names=['vn', 'n', 'ln', 'z', 'lp', 'p', 'vp'])
wout['vn'] = fuzz.zmf(wout.universe, -pi, -pi /4)
wout['n'] = fuzz.trimf(wout.universe, [-pi / 2, -pi / 4, -pi / 8])
wout['ln'] = fuzz.trimf(wout.universe, [-pi / 4, -pi / 8, 0])
wout['z'] = fuzz.trimf(wout.universe, [-pi / 8, 0, pi / 8])
wout['lp'] = fuzz.trimf(wout.universe, [0, pi / 8, pi / 4])
wout['p'] = fuzz.trimf(wout.universe, [pi / 8, pi / 4, pi / 2])
wout['vp'] = fuzz.smf(wout.universe, pi / 4, pi)
#wout.view()


# Construcao do conjunto de regras do controle fuzzy
# REFERENTE APENAS A V
rules = []
rules.append(ctrl.Rule(antecedent=(erro_dist['rrc']), consequent=vout['z'],
                       label='regra muito muito perto'))  # Se o erro é muito muito pequeno, então velocidade é zero

#rules.append(ctrl.Rule(antecedent=(erro_dist['rc'] & d_erro_dist['p']), consequent=vout['lp']))  # Se o erro é muito pequeno e a tendência do erro é aumentar muito, então velocidade é zero
#rules.append(ctrl.Rule(antecedent=(erro_dist['rc'] & d_erro_dist['lp']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['rc'] & d_erro_dist['z']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['rc'] & d_erro_dist['ln']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['rc'] & d_erro_dist['n']), consequent=vout['lp']))

rules.append(ctrl.Rule(antecedent=(erro_dist['c'] & d_erro_dist['z']), consequent=vout['lp'], label='regra perto'))
#rules.append(ctrl.Rule(antecedent=(erro_dist['c'] & d_erro_dist['lp']), consequent=vout['lp']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['c'] & d_erro_dist['p']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['c'] & d_erro_dist['ln']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['c'] & d_erro_dist['n']), consequent=vout['lp']))

rules.append(ctrl.Rule(antecedent=(erro_dist['mc'] & d_erro_dist['z']), consequent=vout['lp']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['mc'] & d_erro_dist['lp']), consequent=vout['z']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['mc'] & d_erro_dist['p']), consequent=vout['z']))
rules.append(ctrl.Rule(antecedent=(erro_dist['mc'] & d_erro_dist['ln']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['mc'] & d_erro_dist['n']), consequent=vout['p']))

rules.append(ctrl.Rule(antecedent=(erro_dist['m'] & d_erro_dist['z']), consequent=vout['lp'], label='regra medio'))
rules.append(ctrl.Rule(antecedent=(erro_dist['m'] & d_erro_dist['n']), consequent=vout['p']))
rules.append(ctrl.Rule(antecedent=(erro_dist['m'] & d_erro_dist['ln']), consequent=vout['p']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['m'] & d_erro_dist['p']), consequent=vout['z']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['m'] & d_erro_dist['lp']), consequent=vout['z']))

rules.append(ctrl.Rule(antecedent=(erro_dist['mf'] & d_erro_dist['z']), consequent=vout['lp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['mf'] & d_erro_dist['ln']), consequent=vout['p']))  # Se erro é meio-longe, então velocidade é moderada
rules.append(ctrl.Rule(antecedent=(erro_dist['mf'] & d_erro_dist['n']), consequent=vout['vp']))  # Se o erro é meio longe e a tendência do erro é diminuir, então a velocidade é muito alta
#rules.append(ctrl.Rule(antecedent=(erro_dist['mf'] & d_erro_dist['lp']), consequent=vout['z']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['mf'] & d_erro_dist['p']), consequent=vout['z']))

rules.append(ctrl.Rule(antecedent=(erro_dist['f'] & d_erro_dist['n']), consequent=vout['vp']))  # Se o erro é muito longe, então a velocidade é alta
rules.append(ctrl.Rule(antecedent=(erro_dist['f'] & d_erro_dist['ln']), consequent=vout['vp']))
rules.append(ctrl.Rule(antecedent=(erro_dist['f'] & d_erro_dist['z']), consequent=vout['p']))
#rules.append(ctrl.Rule(antecedent=(erro_dist['f'] & d_erro_dist['lp']), consequent=vout['z']))
#ules.append(ctrl.Rule(antecedent=(erro_dist['f'] & d_erro_dist['p']), consequent=vout['z']))

rules.append(ctrl.Rule(antecedent=(d_erro_dist['p']), consequent=vout['z']))

rules.append(ctrl.Rule(antecedent=(d_erro_dist['lp']), consequent=vout['z']))


# Construcao do conjunto de regras para theta

rules2 = []

rules2.append(ctrl.Rule(antecedent=(erro_w['z']), consequent=wout['z']))

#rules2.append(ctrl.Rule(antecedent=(erro_w['ln'] & d_erro_w['p']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['ln'] & d_erro_w['lp']), consequent=wout['z']))
rules2.append(ctrl.Rule(antecedent=(erro_w['ln'] & d_erro_w['z']), consequent=wout['ln']))
rules2.append(ctrl.Rule(antecedent=(erro_w['ln'] & d_erro_w['ln']), consequent=wout['ln']))
rules2.append(ctrl.Rule(antecedent=(erro_w['ln'] & d_erro_w['n']), consequent=wout['z']))

rules2.append(ctrl.Rule(antecedent=(erro_w['lp'] & d_erro_w['z']), consequent=wout['lp']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['lp'] & d_erro_w['lp']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['lp'] & d_erro_w['p']), consequent=wout['z']))
rules2.append(ctrl.Rule(antecedent=(erro_w['lp'] & d_erro_w['ln']), consequent=wout['lp']))
rules2.append(ctrl.Rule(antecedent=(erro_w['lp'] & d_erro_w['n']), consequent=wout['lp']))

rules2.append(ctrl.Rule(antecedent=(erro_w['n'] & d_erro_w['z']), consequent=wout['ln']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['n'] & d_erro_w['lp']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['n'] & d_erro_w['p']), consequent=wout['z']))
rules2.append(ctrl.Rule(antecedent=(erro_w['n'] & d_erro_w['ln']), consequent=wout['ln']))
rules2.append(ctrl.Rule(antecedent=(erro_w['n'] & d_erro_w['n']), consequent=wout['n']))

rules2.append(ctrl.Rule(antecedent=(erro_w['p'] & d_erro_w['z']), consequent=wout['lp']))
rules2.append(ctrl.Rule(antecedent=(erro_w['p'] & d_erro_w['n']), consequent=wout['p']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['p'] & d_erro_w['lp']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['p'] & d_erro_w['p']), consequent=wout['z']))
rules2.append(ctrl.Rule(antecedent=(erro_w['p'] & d_erro_w['ln']), consequent=wout['lp']))

rules2.append(ctrl.Rule(antecedent=(erro_w['vn'] & d_erro_w['n']), consequent=wout['vn']))
rules2.append(ctrl.Rule(antecedent=(erro_w['vn'] & d_erro_w['ln']), consequent=wout['vn']))
rules2.append(ctrl.Rule(antecedent=(erro_w['vn'] & d_erro_w['z']), consequent=wout['n']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['vn'] & d_erro_w['lp']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['vn'] & d_erro_w['p']), consequent=wout['z']))

rules2.append(ctrl.Rule(antecedent=(erro_w['vp'] & d_erro_w['n']), consequent=wout['vp']))
rules2.append(ctrl.Rule(antecedent=(erro_w['vp'] & d_erro_w['ln']), consequent=wout['vp']))
rules2.append(ctrl.Rule(antecedent=(erro_w['vp'] & d_erro_w['z']), consequent=wout['p']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['vp'] & d_erro_w['lp']), consequent=wout['z']))
#rules2.append(ctrl.Rule(antecedent=(erro_w['vp'] & d_erro_w['p']), consequent=wout['z']))

rules2.append(ctrl.Rule(antecedent=(d_erro_w['lp']), consequent=(wout['z'])))
rules2.append(ctrl.Rule(antecedent=(d_erro_w['p']), consequent=(wout['z'])))


# Criacao do sistema de controle de v
v_control = ctrl.ControlSystem(rules)
v_control_SIF = ctrl.ControlSystemSimulation(v_control)

# Criacao do sistema de controle de theta
theta_control = ctrl.ControlSystem(rules2)
theta_control_SIF = ctrl.ControlSystemSimulation(theta_control)

# INICIALIZACAO DE PARAMETROS DE SIMULACAO

# Condicoes iniciais
xi = 1
yi = 1
thetai = pi/2

# Pontos de referencia
xref = -5
yref = -10

# Inicializacao de parametros da derivada
dErroDist = 0
dErroTheta = 0
antErroDist = 0
antErroTheta = 0

# Criacao dos passos necessarios para o controle
dt = 0.01  # Passo de integracao
tf = 50
t = np.linspace(0, tf, num=tf / dt + 1)

# Objetivo de armazenar os dados para observacao grafica
x = []
y = []
x.append(xi)
y.append(yi)
theta = thetai



for ta in t:

    erro1 = [xref - x[len(x) - 1], yref - y[len(y) - 1]]
    erro = np.power(erro1, 2)
    distEuc = m.sqrt(erro[0] + erro[1])

#    print('distEuc = ' + str(distEuc))
    #if (distEuc < 0.01):
    #   break

    v_control_SIF.input['erro_dist'] = distEuc
    v_control_SIF.input['d_erro_dist'] = dErroDist

    v_control_SIF.compute()

    v = v_control_SIF.output['vout']

    theta_erro = m.atan2(erro1[1], erro1[0])
    #print('theta_erro1 =' + str(theta_erro))
    theta_erro = theta_erro - theta

    #print('theta_erro =' + str(theta_erro))

    theta_control_SIF.input['erro_w'] = theta_erro
    theta_control_SIF.input['d_erro_w'] = dErroTheta

    theta_control_SIF.compute()

    d_theta = theta_control_SIF.output['wout']

#    print('v=' + str(v))
#    print('d_theta =' + str(d_theta))
    vx = v * m.cos(theta)
    vy = v * m.sin(theta)
    theta = theta + dt * d_theta
    #print('theta = ' + str(theta))

    xa = x[len(x) - 1] + dt * vx
    ya = y[len(y) - 1] + dt * vy

    dErroDist = (distEuc - antErroDist)/dt
    dErroTheta = (theta_erro - antErroTheta)/dt
#    print('dErroDist = ' + str(dErroDist))
    #print('dErroTheta =' + str(dErroTheta))

    antErroDist = distEuc
    antErroTheta = theta_erro

    x.append(xa)
    y.append(ya)

    #print('x =' + str(xa))
    #print('y =' + str(ya))
    #print('-------')



fig = plt.figure()
ax = fig.add_subplot(111)
plt.ion()
plt.xlim(-10,10)
plt.ylim(-10,10)
plt.xlabel('x(m)')
plt.ylabel('y(m)')

fig.show()
fig.canvas.draw()

for i in range(len(x)):
    ax.clear()
    plt.plot(x[i],y[i])
    fig.canvas.draw()

#plt.plot(x,y)
#plt.show()
#x.pop()
#y.pop()
#plt.plot(t, x)
#plt.show()
#plt.plot(t, y)
#plt.show()

