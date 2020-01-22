import numpy as np
import pickle

from GTC import ureal,exp,log,pow,rp,type_a

class gen2500:
    def __init__(self,uncertainty_mode=False):

        self.Ps_input=[] #Saturation pressure PSI
        self.Ts_input=[] #Saturation temperature C
        self.Pc_input=[] #Chamber pressure PSI
        self.Tc_input=[] #Chamber temperature C

        self.Ps=[] #Saturation pressure Pa
        self.Ts=[] #Saturation temperature K
        self.Pc=[] #Chamber pressure Pa
        self.Tc=[] #Chamber temperature K
        self.flow=20 # air flow in liters/min
        self.eta=1 #saturation efficiency coefficient
        self.k=2

        self.RH=[]
        self.DewPoint=[]
        self.SVP_Tc=[] #saturation vapour pressure  for temperature of chamber
        self.SVP_Ts = []  # saturation vapour pressure  for temperature of saturator
        self.f_TcPc=[] #enhancement factor for chamber pressure and temperature
        self.f_TsPs = []  # enhancement factor for chamber pressure and temperature


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
        self.f_TcPc_GTC=ureal(0,0) #enhancement factor for chamber pressure and temperature GTC number
        self.f_TsPs_GTC=ureal(0,0)  # enhancement factor for chamber pressure and temperature GTC number
        self.eta_u_GTC=ureal(0,0)

        # reset data for experiment
        self.N=0 # number of iterations
        self.history=[]
        self.mean=0
        self.std=0

        #initiate new object for storage VISA commands
        self.VISA=VISA()


    def set_values(self,Ps_PSI,Ts_C,Pc_PSI,Tc_C,flow=20,Ps_u_PSI=0,Ts_u_C=0,Pu_u__PSI=0,Tc_u_C=0, eta=1,eta_u=0):

        #print('Ts_C=',Ts_C)
        #write initial values to object
        self.Ps_input=Ps_PSI
        self.Ts_input=Ts_C
        self.Pc_input=Pc_PSI
        self.Tc_input=Tc_C
        self.flow=flow
        self.eta=eta
        self.eta_u=eta_u

        #convert initial values to proper format -! values in PSI and Celsius !!!
        self.Ps_GTC = Ps_PSI if conv.isGTC(Ps_PSI) else ureal(Ps_PSI,Ps_u_PSI,label='Ps')
        self.Ts_GTC = Ts_C if conv.isGTC(Ts_C) else ureal(Ts_C, Ts_u_C, label='Ts')
        self.Pc_GTC = Pc_PSI if conv.isGTC(Pc_PSI) else ureal(Pc_PSI, Pc_u_PSI, label='Pc')
        self.Tc_GTC = Tc_C if conv.isGTC(Tc_C) else ureal(Tc_C, Ts_u_C, label='Tc')
        self.eta_u_GTC = eta if conv.isGTC(eta) else ureal(eta, eta_u, label='eta')

        #conversion of units
        self.Ps_GTC=conv.PSI2Pa(self.Ps_GTC)
        self.Ts_GTC=conv.Celsius2Kelvin(self.Ts_GTC)
        self.Pc_GTC=conv.PSI2Pa(self.Pc_GTC)
        self.Tc_GTC=conv.Celsius2Kelvin(self.Tc_GTC)


        self.DewPoint=[]
        self.SVP_Ts_GTC = conv.calculate_SVP(self.Ts_GTC)  # saturation vapour pressure  for temperature of saturator
        self.SVP_Tc_GTC=conv.calculate_SVP(self.Tc_GTC) #saturation vapour pressure  for temperature of chamber
        self.f_TsPs_GTC =conv.calculate_enh_fact(self.Ts_GTC,self.Ps_GTC) # enhancement factor for saturator pressure and temperature
        self.f_TcPc_GTC = conv.calculate_enh_fact(self.Tc_GTC, self.Pc_GTC)  # enhancement factor for chamber pressure and temperature
        self.RH_GTC=conv.calculate_RH_from_PT(self.Ps_GTC,self.Ts_GTC,self.Pc_GTC,self.Tc_GTC,self.eta_u_GTC)
        self.DewPoint_GTC=conv.calculate_DewPoint2RH(self.RH_GTC,self.Tc_GTC)

        self.SVP_Ts=self.SVP_Ts_GTC.x
        self.SVP_Tc = self.SVP_Tc_GTC.x
        self.f_TsPs=self.f_TsPs_GTC.x
        self.f_TsPs = self.f_TsPs_GTC.x
        self.RH=self.RH_GTC.x
        self.DewPoint=self.DewPoint_GTC.x

        #print('self.SVP_Ts=', self.SVP_Ts)
        #print('self.SVP_Tc=',self.SVP_Tc)
        #print('self.f_TsPs=', self.f_TsPs)
        #print('self.f_TcPc=', self.f_TcPc)
        #print('self.RH_GTC=', self.RH_GTC)

        self.f_TcPc=[] #enhancement factor for chamber pressure and temperature
        self.f_TsPs = []  # enhancement factor for chamber pressure and temperature
        #self.RH = conv.calculate_RH_from_PT(self.Ps_GTC, self.Ts_GTC, self.Pc_GTC, self.Tc_GTC, self.eta_u_GTC)

        # Data for experiment
        self.N+=1
        self.history.append(self.RH_GTC)
        self.mean=type_a.mean(self.history)
        self.std=type_a.standard_uncertainty(self.history) if self.N>1 else 0

        #VISA Datas

    def reset(self):
        Pass



    def summary(self):
        print('\n------------------------------------------------------------')
        print("Summary for humidity generator \n")
        if self.uncertainty_mode==False:
            print('Saturator pressure= {} PSI'.format(self.Ps_input))
            print('Saturator temperature= {} C'.format(self.Ts_input))
            print('Chamber pressure= {} PSI'.format(self.Pc_input))
            print('Chamber temperature= {} C'.format(self.Tc_input))
            print('\n--------------------- Calculations ---------------------')
            print('Relative humidity RH= {} %'.format(self.RH_GTC.x))
            print('Dew point = {} C'.format(self.DewPoint_GTC.x))
            print('Saturation vapour pressure - saturator = {} Pa'.format(self.SVP_Ts_GTC.x))
            print('Saturation vapour pressure - chamber = {} Pa'.format(self.SVP_Tc_GTC.x))
            print('enhancement factor - saturator = {}'.format(self.f_TsPs_GTC.x))
            print('enhancement factor - chamber = {}'.format(self.f_TcPc_GTC.x))
            print('---------------------------------- ---------------------\n')


        else:
            print('Saturator pressure= {} Pa with standard uncertainty {}'.format(self.Ps_GTC.x,self.Ps_GTC.u))
            print('Saturator temperature= {} K with standard uncertainty {}'.format(self.Ts_GTC.x, self.Ts_GTC.u))
            print('Chamber pressure= {} Pa with standard uncertainty {}'.format(self.Pc_GTC.x,self.Pc_GTC.u))
            print('Chamber temperature= {} K with standard uncertainty {}'.format(self.Tc_GTC.x, self.Tc_GTC.u))
            print('\n--------------------- Calculations ---------------------')
            print('Relative humidity RH= {} % with standard uncertainty {}'.format(self.RH_GTC.x,self.RH_GTC.u))
            print('Dew point = {} C with standard uncertainty {}'.format(self.DewPoint_GTC.x,self.DewPoint_GTC.u))
            print('Saturation vapour pressure - saturator = {} Pa with standard uncertainty {}'.format(self.SVP_Ts_GTC.x,self.SVP_Ts_GTC.u))
            print('Saturation vapour pressure - chamber = {} Pa with standard uncertainty {}'.format(self.SVP_Tc_GTC.x,self.SVP_Tc_GTC.u))
            print('enhancement factor - saturator = {}  with standard uncertainty {}'.format(self.f_TsPs_GTC.x,self.f_TsPs_GTC.u))
            print('enhancement factor - chamber = {}  with standard uncertainty {}'.format(self.f_TcPc_GTC.x,self.f_TcPc_GTC.u))
            print('---------------------------------- ---------------------\n')

        print('-------  Uncertainty budget for RH ---------------')
        for cpt in rp.budget(self.RH_GTC):
            print("{0.label}:{0.u:.3f}".format(cpt))

class VISA:
    def __init__(self):
        self.Adres=''
        self.ReadActualValues_command='?'
        self.ReadSetpoints_command='?SP'
        self.ReaRunStatus_command='?R'
        self.ReadErrorNumber_command='?ER'
        self.ReadCabinetFanTemperature='?TF'
        self.Start_command='RUN'
        self.Stop_command='STOP'
        self.PrintSystemData_command='PRINT'
        self.ChangeRH_Pc_Setpoint_command='R1='
        self.ChangeRH_PcTc_Setpoint_command = 'R2='
        self.ChangeSaturationPressurePoint_command='PS='
        self.ChangeSaturationTempSetpoint_command='TS='
        self.ChangeFlowRateSetpoint_command='FS='

        #system attributes
        self.att_RH_Pc_actual=[]
        self.att_RH_PcTc_actual = []
        self.att_Ps_PSI_actual=[]
        self.att_Ts_C_actual=[]
        self.att_Pc_PSI_actual=[]
        self.att_Tc_C_actual=[]
        self.att_Flow_Rate_actual = []
        self.att_System_Status=[]
        self.att_RH_Pc_setpoint= []
        self.att_RH_PcTc_setpoint = []
        self.att_Ps_PSI_setpoint=[]
        self.att_Flow_Rate_setpoint = []
        self.att_Current_Control_Mode=[]
        self.att_Errors=[]
        self.att_Fan_Temperature=[]
    #conversion functions for humidity calculations
class conv:
    #checkin is type GTC uncertainty
    def isGTC(value):
        typeGTC=type(ureal(0,0))
        if type(value)==typeGTC:
            return True
        else:
            return  False
    #converting float type to GTC uncertainty type
    def float2GTC(value):
        if conv.isGTC(value):
            return value
        else:
            return ureal(value,0)

    #converting Pressure in PSI to Pascals
    def PSI2Pa(PSI_value):
        P=conv.float2GTC(PSI_value)
        return 6894.7572931783*P

    #converting Pressure in Pascals to PSI
    def Pa2PSI(Pa_value):
        P=conv.float2GTC(Pa_value)
        return 0.0001450377*P

    #converting temperature in Celsius degrees to Kelvin
    def Kelvin2Celsius(K_value):
        T = conv.float2GTC(K_value)
        return T - 273.15

    #converting temperature in Kelvin degrees to Celsius
    def Celsius2Kelvin(C_value):
        T = conv.float2GTC(C_value)
        return T+273.15

    #calculating saturation vapour pressure
    def calculate_SVP(T_kelvin, method='wexler',medium='water'):
        #possible options method='wexler' or 'sonntag', medium='water' or 'ice'
        T=conv.float2GTC(T_kelvin)
        SVP=ureal(0,0)
        # WEXLER WATER
        if (method=='wexler') and (medium=='water'):
            s06=0 # sum of gi*T^(i-2) for  i=0:6
            g=np.zeros(8)

            g[0]=-2.83657440e3
            g[1] = -6.02807656e3
            g[2] = 1.95426361e1
            g[3] = -2.73783019e-2
            g[4] = 1.62616980e-5
            g[5] = 7.02290560e-10
            g[6] = -1.86800090e-13
            g[7] = 2.71503050

            for i in range(7):
                s06+=g[i]*pow(T,i-2)
            s7=g[7]*log(T)  #gi*ln(T) for  i=7
            s07=s06+s7
            SVP=exp(s07)
        #WEXLER ICE
        elif (method=='wexler') and (medium=='ice'):
            s04=0 # sum of ki*T^(i-1) for  i=0:4
            k=np.zeros(6)

            k[0]=-5.8666426e3
            k[1] =2.2328702e1
            k[2] =1.39387003e-2
            k[3] =-3.42624020e-5
            k[4] =2.7040955e-8
            k[5] =6.70635220e-1

            for i in range(5):
                s04+=k[i]*pow(T,i-1)
            s5=k[5]*log(T)  #ki*ln(T) for  i=5
            s05=s04+s5
            SVP=exp(s05)
        #SONNTAG WATER
        elif (method=='sonntag') and (medium=='water'):
            s03=0 # sum of ki*T^(i-1) for  i=0:3
            g=np.zeros(5)

            g[0]=-6096.9385
            g[1] =21.2409642
            g[2] =-2.711193e-2
            g[3] =1.673952e-5
            g[4] =2.433502

            for i in range(4):
                s03+=g[i]*pow(T,i-1)
            s4=g[4]*log(T)  #gi*ln(T) for  i=4
            s04=s03+s4
            SVP=exp(s04)
        #SONNTAG ICE
        elif (method=='sonntag') and (medium=='ice'):
            s03=0 # sum of ki*T^(i-1) for  i=0:3
            k=np.zeros(5)

            k[0]=-6024.5282
            k[1] =29.32707
            k[2] =1.0613868e-2
            k[3] =-1.3198825e-5
            k[4] =-0.49382577

            for i in range(4):
                s03+=k[i]*pow(T,i-1)
            s4=k[4]*log(T)  #ki*ln(T) for  i=4
            s04=s03+s4
            SVP=exp(s04)
        else:
            print("Error - possible options for function method='wexler' or 'sonntag', medium='water' or 'ice'")

        SVP=SVP+ureal(0,1,label='SVP_aprox')
        return SVP
    #calculate enhancement factor
    def calculate_enh_fact(T_kelvin,P_Pa):
        T = conv.float2GTC(T_kelvin)
        P = conv.float2GTC(P_Pa)

        if T.x<273.15:
            medium='ice'
        else:
            medium='water'

        #calculate vapour pressure eT
        eT=conv.calculate_SVP(T,medium=medium)

        #initialize a,b coefficient
        A=np.zeros(4)
        B=np.zeros(4)
        if medium=='ice':
            A[0]=-5.5898101e-2
            A[1] =6.7140389e-4
            A[2] =-2.7492721e-6
            A[3] =3.8268958e-9
            B[0]=-8.1985393e1
            B[1] =5.8230823e-1
            B[2] =-1.6340527e-3
            B[3] =1.6725084e-6

        elif medium=='water':
            A[0]=-1.6302041e-1
            A[1] =1.8071570e-3
            A[2] =-6.7703064e-6
            A[3] =8.5813609e-9
            B[0]=-5.9890467e1
            B[1] =3.4378043e-1
            B[2] =-7.7326396e-4
            B[3] =6.3405286e-7

        a=ureal(0,0)
        b=ureal(0,0)
        #calculate a coefficient
        for i in range(4):
            a+=A[i]*pow(T,i)

        # calculate b coefficient
        for i in range(4):
            b+=B[i]*pow(T,i)
        b=exp(b)
        s1=a*(1-eT/P)
        s2 = b * (P/eT-1)
        f=exp(s1+s2)
        return f

    def calculate_RH_from_PT(Ps_Pa,Ts_K,Pc_Pa,Tc_K,eta=1,verbose=False):
        Ps = conv.float2GTC(Ps_Pa)
        Ts = conv.float2GTC(Ts_K)
        Pc = conv.float2GTC(Pc_Pa)
        Tc = conv.float2GTC(Tc_K)
        #eta = conv.float2GTC(eta)

        if Ps.label=='': Ps.label='Ps'
        if Ts.label=='': Ts.label='Ts'
        if Pc.label=='': Pc.label='Pc'
        if Tc.label=='': Tc.label='Tc'
        #if eta.label == '': eta.label = 'eta'

        eTs=conv.calculate_SVP(Ts)
        eTc=conv.calculate_SVP(Tc)
        fTsPs=conv.calculate_enh_fact(Ts,Ps)
        fTcPc=conv.calculate_enh_fact(Tc,Pc)

        RH=(Pc/Ps)*(fTsPs/fTcPc)*(eTs/eTc)*100*eta

        if verbose==True:
            print('Uncertainty budget')
            for cpt in rp.budget(RH):
                print("{0.label}:{0.u:.3f}".format(cpt))
        return RH
    def calculate_DewPoint2RH(RH,T_Kelvin):
        #Calculation according to The relationship between Relative Humidity and the Dewpoint Temperature in moist Air, Mark G. Lawrence
        RH = conv.float2GTC(RH)
        T_Kelvin = conv.float2GTC(T_Kelvin)
        T_Celsius=conv.Kelvin2Celsius(T_Kelvin)
        #constants
        A1=17.625
        B1=243.03 #Celsius

        numerattor=B1*(log(RH/100)+A1*T_Celsius/(B1+T_Celsius))
        denominator=A1-log(RH/100)-A1*T_Celsius/(B1+T_Celsius)

        DewPoint=numerattor/denominator
        return DewPoint
########################################################3



Ps=ureal(14.7,7e-5,label='Ps')
Ts=ureal(2,0.01,label='Ts')
Pc=ureal(14.65,7e-5,label='Pc')
Tc=ureal(31,0.01,label='Tc')
eta=ureal(1,0.001,label='eta')



#RH=conv.calculate_RH_from_PT(Ps,Ts,Pc,Tc,verbose=True,eta=eta)
#print('RH value=',RH.x,'U(f)=',2*RH.u)

#Real data from generator
gen=gen2500(uncertainty_mode=True)

Ps_PSI=ureal(14.7,7e-5,label='Ps')
Ts_C=ureal(2,0.01,label='Ts')
Pc_PSI=ureal(14.65,7e-5,label='Pc')
Tc_C=ureal(31,0.01,label='Tc')


#eta=ureal(1,0.01,label='eta')
for i in range(5):
    gen.set_values(Ps_PSI=Ps_PSI,Ts_C=Ts_C,Pc_PSI=Pc_PSI,Tc_C=Tc_C)
    print('N=',gen.N, 'mean=',gen.mean, 'RHi=', gen.history[i])


print('RH=',gen.RH_GTC.x,gen.RH_GTC.u)


with open('gen.pickle', 'wb') as f:
    pickle.dump(gen, f)

with open('gen.pickle', 'rb') as f:
    var_you_want_to_load_into = pickle.load(f)

#print( 'RH=',conv.calculate_DewPoint2RH(65,293.15))


gen.summary()