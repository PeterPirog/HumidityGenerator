import pyvisa
import time

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


for i in range(10):
    command='ROUT:CLOS (@{})'.format(str(i+1))
    inst.write_ascii_values(command,'')
    time.sleep(1)
    inst.query("*OPC?")
    print(inst.query('FETCH?'))
