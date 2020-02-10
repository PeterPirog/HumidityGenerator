import numpy as np
import time
import matplotlib.pyplot as plt


class Channel():
    def __init__(self,chnnel_name='chan_1'):
        self.channel_name=chnnel_name
        self.reset()

    def reset(self):
        self.x=[]
        self.n_items=0
        self.mean=0
        self.mean_series=[]
        self.variance_of_x=0
        self.variance_of_x_series=[]
        self.std_of_x=0
        self.std_of_x_series=[]
        self.std_of_mean = 0
        self.std_of_mean_series=[]
        self.S=0 # variable important for Welford's online algorithm  in function calculate_mean_std()
        self.time_start=[]
        self.time_stamps=[]


    def add(self, x,verbose=False,plot=False):
        self.n_items+=1
        self.x.append(float(x))
        self.calculate_mean_std(verbose=verbose)
        if plot==True:
            self.plot(x_type='x')

    def __str__(self):
        # WYMAGA POPRAWY
        x=map(str,self.x)
        return x


    def calculate_mean_std(self,verbose=False):
        # Welford's online algorithm  https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance https://www.embeddedrelated.com/showar
        k=self.n_items
        x=self.x[self.n_items - 1]

        if k==1:
            self.mean=x
            self.S=0
        else:
            mean_old=self.mean
            self.mean=mean_old+(x-mean_old)/k
            self.S=self.S+(x-mean_old)*(x-self.mean)
            self.variance_of_x=self.S/(k-1)
            self.std_of_x=(self.variance_of_x)**0.5
            self.std_of_mean=self.std_of_x/k**0.5

        #Historical data preparation
        self.mean_series.append(self.mean)
        self.std_of_x_series.append(self.std_of_x)
        self.std_of_mean_series.append(self.std_of_mean)
        self.variance_of_x_series.append(self.variance_of_x)

        self.np_x=np.asarray(self.x)
        self.np_mean=np.asarray(self.mean_series)
        self.np_std_of_x=np.asarray(self.std_of_x_series)
        self.np_std_of_mean=np.array(self.std_of_mean_series)

        if verbose==True:
            print("x=",self.x[self.n_items - 1],
                  "| n_items=",self.n_items,
                  "| mean=", self.mean,
                  "| std_of_x=", self.std_of_x,
                  "| var_of_x=",self.variance_of_x,
                  "| std_of_mean=",self.std_of_mean,"\n")
    def plot(self,y_type='mean',x_type='iterations'):
        if y_type=='x':
            Y=self.np_x
        elif y_type=='mean':
            Y = self.np_mean
        elif y_type=='std':
            Y = self.np_std_of_x
        elif y_type=='std_of_mean':
            Y = self.np_std_of_mean
        else:
            print("wrong y_type parameter, available options: 'x','mean','std','std_of_mean'")

        if x_type=='iterations':
            X=np.asarray(range(len(Y)))
        elif x_type=='time':
            X = np.asarray(range(len(Y)))
        else:
            print("wrong y_type parameter, available options: 'iterations','time'")

        try:
            plt.scatter(X,Y)
            plt.show()
        except:
            pass