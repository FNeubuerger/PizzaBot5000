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
    n_cheeses = np.random.random_integers(1,max_n_cheeses)
    n_sauces = np.random.random_integers(1,max_n_sauces)
    #assemble pizza
    pizza = toppings.sample(n_toppings)

    return pizza



if __name__ == '__main__':
    print(generate_pizza())
