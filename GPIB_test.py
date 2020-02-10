import pyvisa
import time

from MeasurementDataDtorage import Channel

rm = pyvisa.ResourceManager()
print(rm.list_resources())

inst = rm.open_resource('GPIB0::16::INSTR')
print(inst.query("*IDN?"))
inst.write_ascii_values('SYST:PRES','')
time.sleep(1)
inst.write_ascii_values('FUNC "FRES"','')
inst.write_ascii_values('FRES:RANG 100','')
inst.write_ascii_values('TRIG:DELAY 0','')
inst.query("*OPC?")

inst.write_ascii_values('ROUT:CLOS (@2)', '')
inst.query("*OPC?")
time.sleep(1)
print(inst.query('FETCH?'))

data=Channel()
for j in range(20) :

    for i in range(1):
        command='ROUT:CLOS (@{})'.format(str(i+1))
        inst.write_ascii_values(command,'')
        meas=float(inst.query('MEAS:FRES?'))
        data.add(meas,verbose=False)
        print('Channel {} measure: {} ohms'.format(i + 1,meas))
    #time.sleep(1)



data.plot(y_type='x')
print(data.np_x)




