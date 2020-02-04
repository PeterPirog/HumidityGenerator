




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
        self.S=0

    def add(self, x):
        self.n_items+=1
        self.x.append(float(x))
        #print(self.x)
        #self.calculte_iter_mean()
        #self.calculate_iter_std()
        self.calculate_mean_std()

    def __str__(self):
        # WYMAGA POPRAWY
        x=map(str,self.x)
        return x


    def calculate_mean_std(self):
        # Welford's online algorithm  https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance https://www.embeddedrelated.com/showar
        k=self.n_items
        x=self.x[self.n_items - 1]

        if k==1:
            self.mean=x
            self.S=0
        else:
            self.mean_old=self.mean
            self.mean=self.mean_old+(x-self.mean_old)/k
            self.S=self.S+(x-self.mean_old)*(x-self.mean)
            self.variance_of_x=self.S/(k-1)
            self.std_of_x=(self.variance_of_x)**0.5
            self.std_of_mean=self.std_of_x/k**0.5

        print("x=",self.x[self.n_items - 1],
              "| n_items=",self.n_items,
              "| mean=", self.mean,
              "| std_of_x=", self.std_of_x,
              "| var_of_x=",self.variance_of_x,
              "| std_of_mean=",self.std_of_mean,"\n")