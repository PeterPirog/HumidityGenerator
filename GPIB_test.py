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
for j in range(0) :

    for i in range(10):
        command='ROUT:CLOS (@{})'.format(str(i+1))
        inst.write_ascii_values(command,'')
        #time.sleep(1)
        #a=float(inst.query("*OPC?"))
        #print('Channel',i+1,'  ',inst.query('FETCH?'))
        #print('Channel', i + 1, '  ', inst.query('READ?'))
        meas=float(inst.query('MEAS:FRES?'))
        data.add(meas)

        print('Channel {} measure: {} ohms'.format(i + 1,meas))
    #time.sleep(1)

data2=Channel()
data2.add(2)
data2.add(5)
data2.add(1)
data2.add(3)
data2.add(5)
data2.add(6)
data2.add(3)
data2.add(0)
data2.add(-2)
data2.add(4)
data2.add(7)

#print(data2.x)



