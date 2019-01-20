import numpy as np
import random
import facebook
from pandas import read_csv
from argparse import ArgumentParser

def generate_pizza(bases='base.txt', toppings='toppings.txt', cheeses='cheese.txt', sauces='sauce.txt',
                    min_n_toppings=2, max_n_toppings=4, max_n_cheeses=1, max_n_sauces=1,
                    n_cheeses=1, n_toppings=2, n_sauces=1,
                    rand=True):
    #read data
    bases = read_csv(bases, header=None)
    toppings= read_csv(toppings, header=None)
    cheeses = read_csv(cheeses, header= None)
    sauces = read_csv(sauces, header=None)

    #determine number of toppings sauces and cheeses if rand==True
    if rand==True:
        n_toppings = np.random.random_integers(min_n_toppings,min(max_n_toppings,len(toppings)))
        n_cheeses = np.random.random_integers(1,min(max_n_cheeses,len(cheeses)))
        n_sauces = np.random.random_integers(1,min(max_n_sauces,len(sauces)))

    #assemble pizza
    pizza = cheeses.sample(n_cheeses)[0].tolist()+toppings.sample(n_toppings)[0].tolist()+sauces.sample(n_sauces)[0].tolist()+bases.sample(1)[0].tolist()

    return pizza

def format(pizza):
    #print to commandline for facebook display
    for i in range(len(pizza)):
        print(pizza[i])
        

def getPizzaString():
    pizzastr = ""
    for i in range(len(pizza)):
        pizzastr = pizzastr + "\n" + pizza[i]
    return pizzastr

def str2bool(v):
    #stuff for the argparser to understand bools
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def getToken():
    filepath = 'secret.txt'  
    with open(filepath) as fp:  
        token = fp.readline()
    return token

def post():
    #do a facebook post
    graph = facebook.GraphAPI(access_token=getToken(), version = "3.1")
    graph.put_object(parent_object='me', connection_name='feed',
                    message=getPizzaString())

if __name__ == '__main__':
    #get commandline arguments if needed
    parser = ArgumentParser()
    parser.add_argument('--n_ch', help='enter number of exact amount of cheeses, default=1', default=1, type=int)
    parser.add_argument('--n_top', help='enter number of exact amount of toppings, default=2', default=2, type=int)
    parser.add_argument('--n_sauces', help='enter number of exact amount of sauces, default=1', default=1, type=int)
    parser.add_argument('--max_ch', help='enter number of minimum amount of cheeses, default=1', default=1, type=int)
    parser.add_argument('--min_top', help='enter number of minimum amount of toppings, default=2', default=2, type=int)
    parser.add_argument('--max_top', help='enter number of maximum amount of toppings, default=4', default=4, type=int)
    parser.add_argument('--max_sauce', help='enter number of maximum numbers of sauces, default=1', default=1, type=int)
    parser.add_argument('--random', help='determine if number of pizza toppings etc. is random, default=True', default=True, type=str2bool)
    args = parser.parse_args()
    #make my pizza now
    pizza = generate_pizza(min_n_toppings=args.min_top, max_n_toppings=args.max_top, max_n_cheeses=args.max_ch, max_n_sauces=args.max_sauce, n_cheeses=args.n_ch, n_toppings=args.n_top, n_sauces=args.n_sauces, rand=args.random)
    format(pizza)

    #post to facebook
    post()
