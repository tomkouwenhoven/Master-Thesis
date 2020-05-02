# this is the main python code which you should run from terminal

import argparse


def Run(args):
    pass






















def main(args = None):
    #-- 

    parser = argparse.ArgumentParser(description="process some values")
    parser.add_argument('--prosocial', '-ps', type = int, dest = 'prosocial', help = 'The starting pro sociality chance for each agent', default = 0.2)
    parser.add_argument('--generations', '-g', type = int, dest = 'generations', help ='The number of generations', default = 200)
    parser.add_argument('--nrounds', '-nr', type = int, dest = 'nrounds', help ='The number rounds for each generation', default = 30)
    args = parser.parse_args()

    print(args)
        
    Run(args)

if __name__ == "__main__":
    main()

