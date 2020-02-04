




#def calculate_fx(formula,x):
 #   formula=lambda x: x**2
  #  return formula(x)

class Channel():
    def __init__(self,chnnel_name='chan_1'):
        self.channel_name=chnnel_name
        self.reset()

    def reset(self):
        self.x=[]
        self.n_items=0
        self.mean=0
        self.mean_old=0
        self.variance_of_x=0
        self.variance_of_x_old = 0
        self.std_of_x=0
        self.std_of_x_old = 0
        self.std_of_mean = 0
        self.std_of_mean_old = 0

    def add(self, x):
        self.n_items+=1
        self.x.append(float(x))
        #print(self.x)
        self.calculte_iter_mean()
        self.calculate_iter_std()


    def __str__(self):
        # WYMAGA POPRAWY
        x=map(str,self.x)
        return x

    def calculte_iter_mean(self,old_mean=[], x=[], x_idx=[]):
        #self.mean = calculte_iter_mean(self.mean, self.x[self.n_items - 1], self.n_items)
        """
        FORMULA: m(i)=m(i-1)+(x-m(i-1))/i

        :param old_mean: value of previous mean m(i-1)
        :param x: new x value added to recalculate new value
        :param x_idx:
        :return: new recalculated mean m(i)
        """
        if old_mean== []: old_mean = self.mean
        if x==[]: x = self.x[self.n_items - 1]
        if x_idx==[]: x_idx = self.n_items

        self.mean_old=old_mean

        new_mean = old_mean + (x - old_mean) / x_idx
        self.mean=new_mean
        #print("mean=", self.mean, "old mean=", self.mean_old)

    def calculate_iter_std(self,old_std=[], old_mean=[], new_mean=[], x=[], x_idx=[]):


        if old_std== []: old_std = self.std_of_x
        if old_mean==[]:old_mean=self.mean_old
        if new_mean==[]:new_mean=self.mean
        if x==[]: x = self.x[self.n_items - 1]
        if x_idx==[]: x_idx = self.n_items



        self.std_of_x_old=old_std
        old_variance = old_std ** 2
        self.variance_of_x_old=old_variance
        new_variance = old_variance + (x - old_mean) * (x - new_mean)
        self.variance_of_x=new_variance
        new_std = (new_variance) ** 0.5
        self.std_of_x=new_std
        print("x=",self.x[self.n_items - 1],
              "| n_items=",self.n_items,
              "| mean=", self.mean,
              "| old mean=", self.mean_old,
              "| std_of_x=", self.std_of_x,
              "| std_of_x_old=", self.std_of_x_old,
              "| var_of_x=",self.variance_of_x,
              "| var_of_x_old=", self.variance_of_x_old,
              "| std_of_mean=",self.std_of_mean,
              "| std_of_mean_old=",self.std_of_mean_old,"\n")