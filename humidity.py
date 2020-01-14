import numpy as np

class hum:
    def K2C(TempK):
        TempC=TempK-273.15
        return TempC
    def C2K(TempC):
        TempK=TempC+273.15
        return TempK