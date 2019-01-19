import numpy as np
import random
from pandas import read_csv

def generate_pizza(bases='base.txt' ,toppings='toppings.txt',cheeses='cheese.txt',sauces='sauce.txt',min_n_toppings=2,max_n_toppings=4,max_n_cheeses=1,max_n_sauces=1):
    #read data
    bases = read_csv(bases, header=None)
    toppings= read_csv(toppings, header=None)
    cheeses = read_csv(cheeses, header= None)
    sauces = read_csv(sauces, header=None)

    #determine number of toppings sauces and cheeses
    n_toppings = np.random.random_integers(min_n_toppings,min(max_n_toppings,len(toppings)))
    n_cheeses = np.random.random_integers(1,min(max_n_cheeses,len(cheeses)))
    n_sauces = np.random.random_integers(1,min(max_n_sauces,len(sauces)))

    #assemble pizza
    pizza = cheeses.sample(n_cheeses)[0].tolist()+toppings.sample(n_toppings)[0].tolist()+sauces.sample(n_sauces)[0].tolist()+bases.sample(1)[0].tolist()

    return pizza

def format(pizza):
    for i in range(len(pizza)):
        print(pizza[i])

if __name__ == '__main__':
    pizza= generate_pizza()
    format(pizza)
