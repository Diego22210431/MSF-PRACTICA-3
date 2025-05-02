"""
Práctica 4: Sistema cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Diego Raul Torres Velez
Número de control: 22210429
Correo institucional: l22210429@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt 
import control as ctrl
 
# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N=round((tend-t0)/dt)+1
t=np.linspace(t0,tend,N) 
u=np.sin(2*m.pi*95/60*t)+0.8

signal=["Sistema","Hipertenso","Hipotenso"]

def cardio(Z,C,R,L):
    num=[L*R,R*Z]
    den=[C*L*R*Z,L*R+L*Z,R*Z]
    sys=ctrl.tf(num,den)
    return sys
    
    
#Función de transferencia: Individuo Hipotenso [caso]
Z,C,R,L= 0.020, 0.250, 0.600, 0.005
sysS= cardio(Z,C,R,L)
print('Individuo Hipotenso [caso]:')
print(sysS)

#Función de transferencia: Individuo Normotenso [control]
Z,C,R,L= 0.033, 1.500, 0.950, 0.010
sysE= cardio(Z,C,R,L)
print('Individuo Normotenso [control]:')
print(sysE)

#Función de transferencia: Individuo Hipertenso [caso]
Z,C,R,L=0.050, 2.500, 1.400, 0.020
sysF= cardio(Z,C,R,L)
print('Individuo Hipertenso [caso]:')
print(sysF)


#Colores 
morado = [.6,.2,.5]
rojo= [1,0,0]
amarillo=[1,.7,0]
azul= [.1,.5,.7]

# Respuesta del sistema en lazo abierto y en lazo cerrado
def plotsignals(u,sysS,sysE,sysF,signal):
    fig=plt.figure()
    
    if signal=="Sistema":
        ts,Vs=ctrl.forced_response(sysS,t,u,x0)
        plt.plot(ts,Vs, '--', color = azul, label = '$P_p(t): Hipotenso$')
        
        ts,Ve=ctrl.forced_response(sysE,t,u,x0)
        plt.plot(ts,Ve, '-', color = rojo, label = '$P_p(t): Normotenso$')
        
        ts,Vd=ctrl.forced_response(sysF,t,u,x0)
        plt.plot(ts,Vd, ':', color = morado, label = '$P_p(t): Hipertenso$')
    
    elif signal=="Hipertenso":
        ts,Ve=ctrl.forced_response(sysS,t,u,x0)
        plt.plot(ts,Ve, '-', color = rojo, label = '$P_p(t): Control$')
            
        ts,Vd=ctrl.forced_response(sysE,t,u,x0)
        plt.plot(ts,Vd, ':', color = morado, label = '$P_p(t): Hipertenso$')
            
        ts,pid=ctrl.forced_response(sysF,t,u,x0)
        plt.plot(ts,pid, ':',linewidth=3, color = morado, label = '$Pa(t): Tratamiento$')
            
        
    elif signal=="Hipotenso":
       ts,Ve=ctrl.forced_response(sysS,t,u,x0)
       plt.plot(ts,Ve, '-', color = rojo, label = '$P_p(t): Control$')
      
       ts,Vd=ctrl.forced_response(sysE,t,u,x0)
       plt.plot(ts,Vd, ':', color = morado, label = '$P_p(t): Hipotenso$')
        
       ts,pid=ctrl.forced_response(sysF,t,u,x0)
       plt.plot(ts,pid, ':',linewidth=3, color = morado, label = '$Pa(t): Tratamiento$')
     

    plt.grid(False)
    plt.xlim(0,10)
    plt.ylim(-0.5,2)
    plt.xticks(np.arange(0,10,1))
    plt.yticks(np.arange(-0.5,2,.5))
    plt.xlabel('$t$ [s]',fontsize=11)
    plt.ylabel('$V(t)$ [V]',fontsize=11)
    plt.legend(bbox_to_anchor=(0.5,-0.3),loc='center',ncol=4, fontsize=8,frameon=False)
    plt.show()
    fig.set_size_inches(20,5)
    fig.tight_layout()
    namepng='python_'+signal+ '.png'
    namepdf='python_'+signal+ '.pdf'
    fig.savefig(namepng,dpi=600,bbox_inches='tight')
    fig.savefig(namepdf,bbox_inches='tight')
    fig.savefig('.pdf',bbox_inches='tight')

def tratamiento (sys): 
        Cr=10E-6
        Ki=1035.71406250139
        Kp=8.92851562535347e-05
        Re=1/(Ki*Cr)
        Rr=Kp*Re
        numPI=[Rr*Cr,1]
        denPI=[Re*Cr,0]
        PID=ctrl.tf(numPI,denPI)
        X=ctrl.series(PID,sysE)
        sys=ctrl.feedback(X,1,sign=-1)
        return sys
    
def tratamientoH(sysE):
        Cr=10E-6
        Ki=13686.5342163355
        Re=1/(Cr*Ki)
        numI=[1]
        denI=[Re*Cr,0]
        I=ctrl.tf(numI,denI)
        X=ctrl.series(I,sysE)
        sys=ctrl.feedback(X,1,sign=-1)
        return sys
    
#Sistema de control en lazo cerrado
sysPID=tratamiento(sysF)
sysPIH=tratamientoH(sysS)
plotsignals(u,sysS,sysE,sysF,"Sistema")
plotsignals(u,sysE,sysF,sysPID,"Hipertenso")
plotsignals(u,sysE,sysS,sysPIH,"Hipotenso")




