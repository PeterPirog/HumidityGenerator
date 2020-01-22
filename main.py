
from humidity import  gen2500
from GTC import ureal



gen=gen2500(uncertainty_mode=True)

Ps_PSI=ureal(14.7,7e-5,label='Ps')
Ts_C=ureal(2,0.01,label='Ts')
Pc_PSI=ureal(14.65,7e-5,label='Pc')
Tc_C=ureal(31,0.01,label='Tc')


gen.set_values(Ps_PSI=Ps_PSI,Ts_C=Ts_C,Pc_PSI=Pc_PSI,Tc_C=Tc_C)

gen.summary()

print('RH=',gen.RH)
