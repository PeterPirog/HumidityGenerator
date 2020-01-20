import numpy as np
from GTC import ureal

class gen2500:
    def __init__(self,uncertainty_mode=False):
        self.Ps=[] #Saturation pressure
        self.Ts=[] #Saturation temperature
        self.Pc=[] #Chamber pressure
        self.Tc=[] #Chamber pressure
        self.flow=20 # air flow in liters/min
        self.eta=1 #saturation efficiency coefficient
        self.k=2

        self.RH=[]
        self.DewPoint=[]
        self.SVP_Tc=[] #saturation vapour pressure  for temperature of chamber
        self.SVP_Ts = []  # saturation vapour pressure  for temperature of saturator
        self.f_TcPc=[] #enchancement factor for chamber pressure and temperature
        self.f_TsPs = []  # enchancement factor for chamber pressure and temperature


        #data for GTC uncertainty mode
        self.uncertainty_mode=uncertainty_mode  # True if GTC uncertainty calculations available
        self.Ps_u=0 #Saturation pressure standard uncertainty
        self.Ts_u=0 #Saturation temperature standard uncertainty
        self.Pc_u=0 #Chamber pressure standard uncertainty
        self.Tc_u=0 #Chamber pressure standard uncertainty
        self.eta_u = 0 ##saturation efficiency coefficient standard uncertainty, 1%=0.01

        self.Ps_GTC=ureal(0,0) #Saturation pressure GTC number
        self.Ts_GTC=ureal(0,0) #Saturation temperature GTC number
        self.Pc_GTC=ureal(0,0) #Chamber pressure GTC number
        self.Tc_GTC=ureal(0,0) #Chamber pressure GTC number


        self.RH_GTC=ureal(0,0) #GTC number
        self.DewPoint_GTC=ureal(0,0) #GTC number
        self.SVP_Tc_GTC=ureal(0,0) #saturation vapour pressure  for temperature of chamber GTC number
        self.SVP_Ts_GTC=ureal(0,0)  # saturation vapour pressure  for temperature of saturator GTC number
        self.f_TcPc_GTC=ureal(0,0) #enchancement factor for chamber pressure and temperature GTC number
        self.f_TsPs_GTC=ureal(0,0)  # enchancement factor for chamber pressure and temperature GTC number
        self.eta_u_GTC=ureal(self.eta,self.eta_u,label="Etha")

    def set_values(self,Ps_PSI,Ts_C,Pc_PSI,Tc_C,flow=20,Ps_u__PSI=0,Ts_u_C=0,Pu_u__PSI=0,Tc_u_C=0):

        Pass


    def summary(self):
        print("Summary for humidity generator \n")
        if self.uncertainty_mode==False:
            print('Saturator pressure= {} PSI'.format(self.Ps_GTC.x))
            print('Saturator temperature= {} C'.format(self.Ts_GTC.x))
            print('Chamber pressure= {} PSI'.format(self.Pc_GTC.x))
            print('Chamber temperature= {} C'.format(self.Tc_GTC.x))
            print('\n--------------------- Calculations ---------------------')
            print('Relative humidity RH= {} %'.format(self.RH_GTC.x))
            print('Dew point = {} C'.format(self.DewPoint_GTC.x))
            print('Saturation vapour pressure - saturator = {} Pa'.format(self.SVP_Ts_GTC.x))
            print('Saturation vapour pressure - chamber = {} Pa'.format(self.SVP_Tc_GTC.x))
            print('Enchancement factor - saturator = {} Pa'.format(self.f_TsPs_GTC.x))
            print('Enchancement factor - chamber = {} Pa'.format(self.f_TcPc_GTC.x))


        else:
            print('Saturator pressure= {} PSI with standard uncertainty {}'.format(self.Ps_GTC.x,self.Ps_GTC.u))
            print('Saturator temperature= {} C with standard uncertainty {}'.format(self.Ts_GTC.x, self.Ts_GTC.u))
            print('Chamber pressure= {} PSI with standard uncertainty {}'.format(self.Pc_GTC.x,self.Pc_GTC.u))
            print('Chamber temperature= {} C with standard uncertainty {}'.format(self.Tc_GTC.x, self.Tc_GTC.u))
            print('\n--------------------- Calculations ---------------------')
            print('Relative humidity RH= {} % with standard uncertainty {}'.format(self.RH_GTC.x,self.RH_GTC.u))
            print('Dew point = {} C with standard uncertainty {}'.format(self.DewPoint_GTC.x,self.DewPoint_GTC.u))
            print('Saturation vapour pressure - saturator = {} Pa with standard uncertainty {}'.format(self.SVP_Ts_GTC.x,self.SVP_Ts_GTC.u))
            print('Saturation vapour pressure - chamber = {} Pa with standard uncertainty {}'.format(self.SVP_Tc_GTC.x,self.SVP_Tc_GTC.u))
            print('Enchancement factor - saturator = {} Pa with standard uncertainty {}'.format(self.f_TsPs_GTC.x,self.f_TsPs_GTC.u))
            print('Enchancement factor - chamber = {} Pa with standard uncertainty {}'.format(self.f_TcPc_GTC.x,self.f_TcPc_GTC.u))

    #conversion functions
class conv:

    def isGTC(value):
        typeGTC=type(ureal(0,0))
        if type(value)==typeGTC:
            return True
        else:
            return  False

    def PSI2Pa(value):
        pass
        #1 Pa = 0.0001450377 psi


def K2C(TempK):
    TempC=TempK-273.15
    return TempC
def C2K(TempC):
    TempK=TempC+273.15
    return TempK


########################################################3

g=gen2500(uncertainty_mode=True)


g.summary()
a=ureal(2,1)
b=3
print(conv.isGTC(a))
print(conv.isGTC(b))