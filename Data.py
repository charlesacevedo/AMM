'''
1. Create Math equations that gives us price of y in terms of a
2. Create a loop to iterate through and simulate different slippage paths
3. Graph
'''

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt


'''
sigma = 0.2
eta = 0.8
Ufun = function(a,b,y) {
  
  x = (a^(1-sigma) + b^(1-sigma))^(1/(1-sigma))
  U = x^(1-eta) + y^(1-eta)
  
  return(U)
  
}
a0 = 10
b0 = 10
y0 = 10
Ustart = Ufun(a0, b0, y0)
Ufun(a0, b0, y0)
ayprice = function(delA) {
  
  rootfun = function(delY) {
    return(Ufun(a0 + delA, b0, y0 - delY) - Ustart)
  }
  
  
  out = uniroot(rootfun, c(0, 10))$root
  return(out)
  
}
'''



class data_ay():
    def __init__(self, sigma, eta, a0, b0, y0):
        self.sigma = sigma
        self.eta = eta
        self.a = a0
        self.b = b0
        self.y = y0
      
    def Ufun(self, a, b, y):
        x = (a**(1-self.sigma) + b**(1-self.sigma))**(1/(1-self.sigma))
        U = x**(1-self.eta) + y**(1-self.eta)
        return(U)

    def quantity(self, delA):
        UStart = self.Ufun(self.a, self.b, self.y)
        delY = opt.root(lambda delY: self.Ufun(self.a + delA, self.b, self.y - delY) - UStart, 3.41)
        
        return delY

    def price(self, delA):
        delY = self.quantity(delA).x[0]
        ratio = delA / delY

        return ratio

    def slippage(self, delA):
        return (((self.price(delA) / self.price(1)) - 1) * 100)



    # def update_a(self, delA):
    #     self.a = self.start(self.a0) + ((1 + self.f) * delA)
        
    # def update_y(self, self.quantity(delA))
    #     self.y0 = self.start(self.y0) - quantity(delA)
 
    # def count(self, a0, b0, y0):
    #     self.a0 = self.update_a(delA)
    #     self.y0 = self.update_y(self.quantity(delA))


    # def limit(self, delA):
    #   y0 = self.y
    #   y0 = y0 - self.quantity(delA).x[0]
    #   if int(y0) > 0:
    #     print(1) 
    #   else:
    #     print('More liquidity must be locked in asset Y before swap can be executed.')


d = data_ay(.2, .8, 100, 100, 100)
UStart_ay = d.Ufun(d.a, d.b, d.y)
UStart_ay

'''
Running Diagnostic tests for AY swaps
'''
# print(d.limit())
# delY = d.quantity(3)
# print(delY.x[0])
# print(d.price(3))
# d.quantity(3).x[0]
# print(d.quantity(3).x[0]), 0.56, 1.084
# print(d.quantity(35).x[0])
# print(d.slippage(3, 1))
# print(d.slippage(5))
# print((d.price(3)/d.price(1) - 1) * 100)


'''
Graph of incremental Y received for 1 unit increases in A.
'''
delA = [i for i in range(100)]
difference = [(d.quantity(i).x[0]-d.quantity(i-1).x[0]) for i in range(100)]

plt.plot(delA, difference)
#plt.ylim([0, 1])
#plt.xlim([0, 12])
plt.xlabel('Amount of A added to LP')
plt.ylabel('Incremental Amount of Y Received')
plt.show()


'''
Graph of price slippage
'''
delA = [i for i in range(100)]
slippage = ([d.slippage(i) for i in range(100)])
slippage = np.log10(np.array(slippage))

plt.plot(delA, slippage)
#plt.xlim(0,35)
#plt.ylim(0, 2.2)
plt.xlabel('Amount of A being exchanged for Y')
plt.ylabel('Price Slippage of Expected Price of Y versus Actual (%)')
plt.show()


'''
slippage as a function of price

how much A you spend in order to get 1 y should be
increasing, while the quantity of A increases
and while the quantity of y decreases.
'''
slippage =np.array([d.slippage(i) for i in range(100)])
price = np.array([d.price(i) for i in range(100)])
price = np.log10(price)
slippage = np.log10(slippage)

plt.plot(price, slippage)
plt.xlabel('Price Y in terms of A, log10')
plt.ylabel('Slippage, log10')
plt.ylim(0, 1.75)
plt.show()




class data_by():
    def __init__(self, sigma, eta, a0, b0, y0):
        self.sigma = sigma
        self.eta = eta
        self.a = a0
        self.b = b0
        self.y = y0
      
    def Ufun(self, a, b, y):
        x = (a**(1-self.sigma) + b**(1-self.sigma))**(1/(1-self.sigma))
        U = x**(1-self.eta) + y**(1-self.eta)
        return(U)

    def quantity(self, delB):
        UStart = self.Ufun(self.a, self.b, self.y)
        delY = opt.root(lambda delY: self.Ufun(self.a, self.b + delB, self.y - delY) - UStart, 3.41)
        
        return delY

    def price(self, delB):
        delY = self.quantity(delB).x[0]
        ratio = delB / delY

        return ratio

    def slippage(self, delB):
        return (((self.price(delB) / self.price(1)) - 1) * 100)




c = data_by(.2, .8, 100, 100, 100)
UStart_by = c.Ufun(c.a, c.b, c.y)




class data_ab():
    def __init__(self, sigma, eta, a0, b0, y0):
        self.sigma = sigma
        self.eta = eta
        self.a = a0
        self.b = b0
        self.y = y0

    def Ufun(self, a, b, y):
        x = (a**(1-self.sigma) + b**(1-self.sigma))**(1/(1-self.sigma))
        U = x**(1-self.eta) + y**(1-self.eta)
        return(U)

    def quantity(self, delA):
        UStart = self.Ufun(self.a, self.b, self.y)
        delB = opt.root(lambda delB: self.Ufun(self.a + delA, self.b - delB, self.y) - UStart, 3.44)

        return delB

    def price(self, delA):
        delB = self.quantity(delA).x[0]
        ratio = delA / delB

        return ratio

    def slippage(self, delA):
        return ((self.price(delA) / self.price(1)) - 1) * 100




b = data_ab(.2, .8, 100, 100, 100)
UStart_ab = b.Ufun(b.a, b.b, b.y)
UStart_ab

# delB = b.quantity(2)
# print(delB.x[0])
# print(b.quantity().x[0])
# print(b.quantity(35).x[0])
# print(b.slippage(2))
# print(b.price(3))
# b.quantity(2).x[0]

'''
Graph of amount of b received per 1 unit increase in A
'''
difference = [(b.quantity(i).x[0]-b.quantity(i-1).x[0]) for i in range(100)]
delA = [i for i in range(100)]
plt.plot(delA, difference)
plt.ylim([0, 2])
# plt.xlim([0, 11])
plt.xlabel('Amount of A added to LP')
plt.ylabel('Amount of B Received per 1 Unit Increase in A')
plt.show()

'''
Graph of price slippage for AB swaps

how much A you spend in order to get 1 B should be
increasing, while the quantity of A increases
and while the quantity of b decreases.
'''
price = np.array([b.price(i) for i in range(100)])
delA = [i for i in range(100)]
quant = [b.quantity(i).x[0] for i in range(100)]
slippage = np.array([b.slippage(i)for i in range(100)])
# slippage = np.log10(slippage)
plt.plot(delA, np.log10(slippage))
# plt.xlim(0,30)
# plt.ylim(0, 10)
plt.xlabel('Amount of A being exchanged for B')
plt.ylabel('Price Slippage of Expected Price of B versus Actual (%)')
plt.show()


outer = np.linspace(0, 101, 50)
inner = np.linspace(0, 101, 50)

discrete_out = [i for i in range(0, 101)]
discrete_in = [i for i in range(0, 101)]

ay_slippage = [d.slippage(i) for i in discrete_out]
by_slippage = [c.slippage(i) for i in discrete_out]
ab_slippage = [b.slippage(i) for i in discrete_in]
cp_slippage = [cp.slippage(i) for i in discrete_in]
ay_slippage = [d.slippage(i) for i in outer]
by_slippage = [c.slippage(i) for i in outer]
ab_slippage = [b.slippage(i) for i in inner]
cp_slippage = [cp.slippage(i) for i in inner]
plt.plot(outer, np.log10(ay_slippage), 'r', label = 'A to Y')
plt.plot(outer, np.log10(by_slippage), 'k:', label = 'B to Y')
plt.plot(inner, np.log10(ab_slippage), label = 'A to B')
plt.plot(inner, np.log10(cp_slippage), label = 'CPMM')
plt.xlim(0, 100)
plt.ylim(0, 2.2)
# plt.xticks([0] + discrete_out)
plt.legend()
plt.title('Comparison of Price Slippage Paths between \nThree-Asset NAMM and CPMM')
plt.xlabel('Amount of Asset Traded in Exchange')
plt.ylabel('Price Slippage %, log10')
plt.show()




class data_CPMM():
    def __init__(self, a0, b0):
        self.a = a0
        self.b = b0

    def Ufun(self, a, b):
        U = self.a * self.b
        return(U)

    def quantity(self, delA):
        UStart = self.Ufun(self.a, self.b)
        delB = opt.root(lambda delB: ((self.a + delA) * (self.b - delB)) - UStart, 1)

        return delB

    def price(self, delA):
        delB = self.quantity(delA).x[0]
        ratio = delA / delB

        return ratio

    def slippage(self, delA):
        return ((self.price(delA) / self.price(1)) - 1) * 100

cp = data_CPMM(100, 100)
UStart_cp = cp.Ufun(cp.a, cp.b)
UStart_cp


'''
Running Diagnostic tests for AY swaps
'''
# delB = cp.quantity(3)
# print(delB.x[0])
# cp.quantity().x[0]
# print(cp.price(9))