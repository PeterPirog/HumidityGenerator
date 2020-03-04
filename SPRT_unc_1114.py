import GTC
import openpyxl
from GTC import ureal
from its90 import Calculate_temp_from_W,Calculate_Wr

def lists2ureal(value_list,unc_list=[],k=2):
    for i,val in enumerate(value_list):
        try:
            d=unc_list[i]
        except:
            unc_list.append(0)
    result = [ureal(value_list_i, unc_list_i / k) for value_list_i, unc_list_i in zip(value_list, unc_list)]
    return result





#Dane ze świadectwa dla typu 5685 nr 1114

R0=ureal(x=2.5534637,u=0.0000041/2,label='R0')

#print(Calculate_Wr(961.78))

#print(Calculate_temp_from_W(1.079488))

#Dane ze świadectwa
t=[961.78,660.332,419.527,231.928]
t_U=[0.0052,0.0040,0.0017,0.0015]
Wt=[4.28556295,3.37543469,2.56855103,1.89259628]

#Konwersja liczb do postaci ureal
t=lists2ureal(t,t_U)
Wt=lists2ureal(Wt)

Wr=map(Calculate_Wr,t)


print('t=',t)
print('Wt=',Wt)
print('Wr=',Wr)

for item in map(Calculate_Wr,t):
    print(item)

path = r'C:\Users\Admin\PycharmProjects\HumidityGenerator\SPRT_nr_1114.xlsx'
book=openpyxl.load_workbook(path)
sheet=book['Swiadectwo']