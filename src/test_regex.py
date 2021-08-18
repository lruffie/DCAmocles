import re

regex = 'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]*\.[0-9]+_level:[0-9]*\.[0-9]+_delta:[0-9]*\.[0-9]+'

def check(email):
    # regex = r'asset:[a-zA-Z]+_base:[a-zA-Z]+_amount:[0-9]*\.[0-9]+_level:[0-9]*\.[0-9]+_delta:[0-9]*\.[0-9]+'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        print("Valid Email")
 
    else:
        print("Invalid Email")

check('asset:eth_base:usdt_amount:200.0_level:3200.0_delta:0.1')


string='asset:eth_base:usdt_amount:1000_level:3200.0_delta:0.1'

def parser(input):
    f=input.split('_')
    dico={}
    for u in f:
        print(u)
        x=u.split(':')
        if x[0] == 'asset' or x[0] =='base' :
            d={str(x[0]):x[1]}
        else :
            d={str(x[0]):float(x[1])}
        dico.update(d)

    return dico
parser(string)