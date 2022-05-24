import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import pyplot_themes as themes
import pandas as pd
themes.theme_ggplot2(figsize=[10, 5])


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

d = data_ay(.2, .8, 100, 100, 100)
UStart_ay = d.Ufun(d.a, d.b, d.y)
UStart_ay



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
Figure Section
'''



#Graph Displaying price slippage paths for NAMM swaps and CPMM swaps
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
plt.plot(inner, np.log10(cp_slippage), label = 'CPMM')
plt.plot(outer, np.log10(ay_slippage), 'r', label = 'A to Y')
plt.plot(outer, np.log10(by_slippage), 'k:', label = 'B to Y')
plt.plot(inner, np.log10(ab_slippage), label = 'A to B')
plt.xlim(0, 100)
plt.ylim(0, 2.2)
plt.legend()
plt.title('Comparison of Price Slippage Paths between \nThree-Asset NAMM and CPMM')
plt.xlabel('Amount of Asset Traded in Exchange')
plt.ylabel('Price Slippage %, log10')
plt.show()
plt.savefig('SlippagePaths.png')



'''
AY Swap graphs
'''
#Plot displaying incremental amount of y received for AY swaps
delA = [i for i in range(100)]
difference = [(d.quantity(i).x[0]-d.quantity(i-1).x[0]) for i in range(100)]

plt.plot(delA, difference)
plt.xlabel('Amount of A added to LP')
plt.ylabel('Incremental Amount of Y Received')
plt.title('AY Swap Return')
plt.themes
plt.show()



#plot displaying AY swaps price slippage as a function of price
slippage =np.array([d.slippage(i) for i in range(100)])
price = np.array([d.price(i) for i in range(100)])
price = np.log10(price)
slippage = np.log10(slippage)

plt.plot(price, slippage)
plt.xlabel('Price of Y in terms of A, log10')
plt.ylabel('Slippage, log10')
plt.ylim(0, 1.75)
plt.title('AY Price Sllippage as a Function of Price')
plt.show()



'''
AB swap graphs
'''
#AB swaps incremental amount of B received per 1 unit increase in A
difference = [(b.quantity(i).x[0]-b.quantity(i-1).x[0]) for i in range(100)]
delA = [i for i in range(100)]

plt.plot(delA, difference)
plt.ylim([0, 2])
# plt.xlim([0, 11])
plt.xlabel('Amount of A added to LP')
plt.ylabel('Amount of B Received per 1 Unit Increase in A')
plt.title('AB Swap Return')
plt.show()



#plot displaying AB swaps price slippage as a function of price
slippage =np.array([b.slippage(i) for i in range(100)])
price = np.array([b.price(i) for i in range(100)])
price = np.log10(price)
slippage = np.log10(slippage)

plt.plot(price, slippage)
plt.xlabel('Price of B in terms of A, log10')
plt.ylabel('Slippage, log10')
plt.title('AB Price Slippage as a Function of Price')
plt.show()



'''
CPMM swap graphs
'''
#AB swaps incremental amount of B received per 1 unit increase in A
difference = [(cp.quantity(i).x[0]-cp.quantity(i-1).x[0]) for i in range(100)]
delA = [i for i in range(100)]

plt.plot(delA, difference)
plt.ylim([0, 2])
plt.xlim([0,100])
plt.xlabel('Amount of A added to LP')
plt.ylabel('Amount of B Received per 1 Unit Increase in A')
plt.title('CPMM Swap Return')
plt.show()



#plot displaying AB swaps price slippage as a function of price
slippage =np.array([cp.slippage(i) for i in range(100)])
price = np.array([cp.price(i) for i in range(100)])
price = np.log10(price)
slippage = np.log10(slippage)

plt.plot(price, slippage)
plt.xlabel('Price of B in terms of A, log10')
plt.ylabel('Slippage, log10')
plt.title('CPMM Price Slippage as a Function of Price')
plt.show()



'''
Conceptual Model graphs
'''



#A Swaps for Y
delA = [i for i in range(100)]
difference = [(d.quantity(i).x[0]-d.quantity(i-1).x[0]) for i in range(100)]

plt.plot(delA, difference)
plt.xlabel('Amount of A added to LP')
plt.ylabel('Incremental Amount of Y Received')
plt.title('AY Swap Return')
plt.themes
plt.show()



#Quantity of Y vs Price of Y
difference = np.array([(d.quantity(i).x[0]-d.quantity(i-1).x[0]) for i in range(100)]) ** 2
price = np.array([d.price(i) for i in range(100)])
price = (price) **2

plt.plot(difference, price)
plt.xlabel('Incremental Amount of Y in LP')
plt.ylabel('Price of Y in Terms of A')
# plt.ylim(0, 1.75)
plt.title('Quantity of Y vs. Price of Y')
plt.xticks(0,100)
plt.show()



#Quantity of A vs. price slippage
slippage =np.array([d.slippage(i) for i in range(100)])
delA = [i for i in range(100)]
slippage = np.log10(slippage)

plt.plot(delA, slippage)
plt.xlabel('Amount of A added to LP')
plt.ylabel('Slippage, log10')
plt.title('Quantity of A in LP vs. Price Slippage of Y')
plt.themes
plt.show()



#Price of y versus price slippage
price = np.array([d.price(i) for i in range(100)])
slippage =np.array([d.slippage(i) for i in range(100)])
slippage = np.log10(slippage)

plt.plot(price, slippage)
plt.xlabel('Price of Y in Terms of A')
plt.ylim(0, 1.8)
plt.ylabel('Slippage, log10')
plt.title('Price vs. Price Slippage of Y')
plt.themes
plt.show()



'''
Exporting data
'''



dict1 = {
    'delA' : [i for i in range(100)], 'Quantity_Returned_Y' : [d.quantity(i).x[0] for i in range(100)], 'Incremental_Y' : [(d.quantity(i).x[0]-d.quantity(i-1).x[0]) for i in range(100)], 'Price_Y' : [d.price(i) for i in range(100)], 'Slippage_Y' : [d.slippage(i) for i in range(100)], 'Quantity_Returned_B' : [b.quantity(i).x[0] for i in range(100)], 'Incremental_B' : [(b.quantity(i).x[0]-b.quantity(i-1).x[0]) for i in range(100)], 'Price_B' : [b.price(i) for i in range(100)], 'Slippage_B' : [b.slippage(i) for i in range(100)], 'Quantity__Returned_CPMM' : [cp.quantity(i).x[0] for i in range(100)], 'Incremental_CPMM' : [(cp.quantity(i).x[0]-cp.quantity(i-1).x[0]) for i in range(100)], 'Price_CPMM' : [cp.price(i) for i in range(100)], 'Slippage_CPMM' : [cp.slippage(i) for i in range(100)]
}
print(dict1)
df = pd.DataFrame.from_dict(dict1, orient='index')
df = df.transpose()
df.to_csv("SimulationData.csv")
