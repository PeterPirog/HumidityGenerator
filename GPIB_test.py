import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()

inst = rm.open_resource('ASRL7::INSTR')
inst.write_termination = '\r'
print(inst.query("?"))