#ITS-90 functionc  calculated  according to "Guide to the realization of the ITS-90", platinum resistance termometry
#import numpy as np
import GTC


def isGTC(value):
    typeGTC = type(GTC.ureal(0, 0))
    if type(value) == typeGTC:
        return True
    else:
        return False

# converting float type to GTC uncertainty type
def float2GTC(value):
    if isGTC(value):
        return value
    else:
        return GTC.ureal(value, 0)


def Conv_celsius2kelvin(temp_c):
    return float2GTC(temp_c+273.15)
def Conv_kelvin2celsius(temp_k):
    return float2GTC(temp_k-273.15)

def Calculate_Wr(temp_C):
    # constants for temperature range -259.3467 C to 0 C
    A=[-2.13534729, #A0
       3.18324720, #A1
       -1.80143597,#A2
       0.71727204, #A3
       0.50344027,#A4
       -0.61899395,#A5
       -0.05332322, #A6
       0.28021362, #A7
       0.10715224, #A8
       -0.29302865,#A9
       0.04459872,#A10
       0.11868632,#A11
       -0.05248134]#A12
    # constants for temperature range 0 C to 961.78 C
    C = [2.78157254,#C0
         1.64650916,#C1
         -0.13714390,#C2
         -0.00649767,#C3
         -0.00234444,#C4
         0.00511868,#C5
         0.00187982,#C6
         -0.00204472,#C7
         -0.00046122,#C8
         0.00045724]#C9

    temp_K=Conv_celsius2kelvin(float(temp_C))
    Wr=1
    if (temp_C>= -259.3467) and (temp_C<0):
        for i in range(13):
            if i==0:
                sum=A[0]
            else:
                sum=sum+A[i]*GTC.pow((GTC.log(temp_K/273.16)+1.5)/1.5,i)
        Wr=GTC.exp(sum)
    elif (temp_C>= 0) and (temp_C<=961.78):
        for i in range(10):
            if i==0:
                sum=C[0]
            else:

                sum=sum+C[i]*GTC.pow((temp_K-754.15)/481,i)
        Wr=sum
    else:
        print("temperature out of range")
    print("Wr({})={}".format(temp_C, Wr))
    return Wr
def Calculate_temp_from_W(W):
    # constants for temperature  calculation range -259.3467 C to 0 C
    B=[0.183324722,#B0
       0.240975303,#B1
       0.209108771,#B2
       0.190439972,#B3
       0.142648498,#B4
       0.077993465,#B5
       0.012475611,#B6
       -0.032267127,#B7
       -0.075291522,#B8
       -0.056470670,#B9
       0.076201285,#B10
       0.123893204,#B11
       -0.029201193,#B12
       -0.091173542,#B13
       0.001317696,#B14
       0.026025526]#B15
    # constants for temperature calculation range 0 C to 961.78 C
    D=[439.932854, #D0
       472.418020, #D1
       37.684494,#D2
       7.472018,#D3
       2.920828,#D4
       0.005184,#D5
       -0.963864,#D6
       -0.188732,#D7
       0.191203,#D8
       0.049025]#D9
    temp_k=0
    if W<=1:
        for i in range(16):
            if i==0:
                sum=B[0]
            else:
                sum=sum+B[i]*GTC.pow((GTC.pow(W,1/6)-0.65)/0.35,i)
        temp_k=273.16*sum
    else:
        for i in range(10):
            if i==0:
                sum=0
            else:
                sum=sum+D[i]*GTC.pow((W-2.64)/1.64,i)
        temp_k=273.15+D[0]+sum
    temp_c = Conv_kelvin2celsius(temp_k)
    print("W({})={}".format(temp_c, W))
    return temp_c
while(1):
    temp=float(input('Set temperature in C: '))

    W=Calculate_Wr(temp)
    T = Calculate_temp_from_W(W)
    print("T=",T)