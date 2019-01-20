#!/usr/bin/env python3
import numpy as np
import random
import facebook
from pandas import read_csv
from argparse import ArgumentParser
import smtplib
import time


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


def getPizzaString(pizza):
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
        user_short_lived_token_from_client = fp.readline()
    filepath = 'appID.txt'
    with open(filepath) as fp:
        app_id = fp.readline()
    filepath = 'appSecret.txt'
    with open(filepath) as fp:
        app_secret = fp.readline()

    graph = facebook.GraphAPI(user_short_lived_token_from_client)
    # Extend the expiration time of a valid OAuth access token.
    extended_token = graph.extend_access_token(app_id, app_secret)
    return extended_token
    
def getpw():
    filepath = 'pw.txt'
    with open(filepath) as fp:
        pw = fp.readline()
    return pw

def post(pizza):
    #do a facebook post
    graph = facebook.GraphAPI(access_token=getToken(), version = "3.1")
    graph.put_object(parent_object='me', connection_name='feed',
                    message=getPizzaString(pizza))


def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    header += 'Cc: %s' % ','.join(cc_addr_list)
    header += 'Subject: %s' % subject
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

def infinite_random_shitposting():
    while True:
        try:
            pizza = generate_pizza(min_n_toppings=args.min_top, max_n_toppings=args.max_top, max_n_cheeses=args.max_ch, max_n_sauces=args.max_sauce, n_cheeses=args.n_ch, n_toppings=args.n_top, n_sauces=args.n_sauces, rand=args.random) #with optional parameters
            if args.post==True:
                post(pizza)
                #only post every 4 hours
                time.sleep(4*60*60)
            else:
                format(pizza)
                print('-----')
                #post every 2 seconds for testing
                time.sleep(2)
        except:
            sendemail(from_addr='pizzabot54321@gmail.com', to_addr_list=['jonas793@gmail.com'], cc_addr_list=['felix793@gmail.com'],
                       subject='PizzaBot Failure',
                       message='whoops something broke again',
                       login='pizzabot54321',
                       password=get_pw()
                       )
            break


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
    parser.add_argument('--post', help='determine if the generated pizza should be posted to facebook, default=False', default=False, type=str2bool)
    parser.add_argument('--loop', help='determine if automatic posting should be done, default=False', default=False, type=str2bool)
    args = parser.parse_args()
    if args.loop==True:
        #if infinity loop is wanted do that
        infinite_random_shitposting() #uses commandline arguments internally
    else:
         #make my pizza now and print it to console and/or post it
         pizza = generate_pizza(min_n_toppings=args.min_top, max_n_toppings=args.max_top, max_n_cheeses=args.max_ch, max_n_sauces=args.max_sauce, n_cheeses=args.n_ch, n_toppings=args.n_top, n_sauces=args.n_sauces, rand=args.random)
         format(pizza)

         if args.post==True:
             #post to facebook
            post(pizza)
